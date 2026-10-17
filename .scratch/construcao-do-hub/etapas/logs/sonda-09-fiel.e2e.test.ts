/**
 * E2E (hub fork): versioned writes against a real CouchDB.
 *
 * Needs a CouchDB given by HUB_TESTE_COUCHDB_URL / _USER / _PASSWORD; skipped
 * without it. `npm run test:e2e:banco` starts a throwaway one (scripts/e2e-banco.mjs).
 * Each run uses a fresh database and deletes it at the end.
 */
import { describe, it, before, after } from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, rm } from "fs/promises";
import { tmpdir } from "os";
import { join } from "path";
import { spawn, type ChildProcess } from "child_process";
import { randomBytes } from "crypto";

const COUCH = process.env.HUB_TESTE_COUCHDB_URL;
const COUCH_USER = process.env.HUB_TESTE_COUCHDB_USER ?? "admin";
const COUCH_PASSWORD = process.env.HUB_TESTE_COUCHDB_PASSWORD ?? "";
const PORT = parseInt(process.env.HUB_TESTE_MCP_PORT ?? "8796");
const BASE = `http://127.0.0.1:${PORT}/mcp`;
const AUTH = "versao-e2e-token";
const DB = `hub-teste-${randomBytes(4).toString("hex")}`;

let server: ChildProcess;
let dataDir: string;
let sessionId = "";
let serverLogs = "";

// --- CouchDB, seen from outside the MCP ---

async function couch(method: string, path: string, body?: unknown): Promise<any> {
    const resp = await fetch(`${COUCH}/${path}`, {
        method,
        headers: {
            "Content-Type": "application/json",
            // open_revs=all answers multipart/mixed unless JSON is asked for.
            "Accept": "application/json",
            "Authorization": "Basic " + Buffer.from(`${COUCH_USER}:${COUCH_PASSWORD}`).toString("base64"),
        },
        body: body === undefined ? undefined : JSON.stringify(body),
    });
    return await resp.json();
}

/** The live leaves of the note at `notePath`: its metadata document, every branch. */
async function leaves(notePath: string): Promise<any[]> {
    const all = await couch("GET", `${DB}/_all_docs?include_docs=true`);
    const row = all.rows.find((r: any) => r.doc?.path === notePath);
    assert.ok(row, `no document for ${notePath} in the database`);
    const revs = await couch("GET", `${DB}/${encodeURIComponent(row.id)}?open_revs=all`);
    return revs.filter((r: any) => r.ok && !r.ok._deleted).map((r: any) => r.ok);
}

/** The text of every live leaf of the note, joined from its chunks (no E2EE in this suite). */
async function leafTexts(notePath: string): Promise<string[]> {
    const texts: string[] = [];
    for (const leaf of await leaves(notePath)) {
        const chunks = await couch("POST", `${DB}/_all_docs?include_docs=true`, { keys: leaf.children });
        texts.push(chunks.rows.map((r: any) => r.doc.data).join(""));
    }
    return texts;
}

// --- MCP over HTTP ---

function parseSSE(raw: string): any {
    for (const line of raw.split("\n")) {
        if (line.startsWith("data: ")) {
            try { return JSON.parse(line.slice(6)); } catch { /* skip */ }
        }
    }
    return JSON.parse(raw);
}

async function mcpCall(method: string, params: any, id = 1): Promise<any> {
    const resp = await fetch(BASE, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": `Bearer ${AUTH}`,
            ...(sessionId ? { "mcp-session-id": sessionId } : {}),
        },
        body: JSON.stringify({ jsonrpc: "2.0", id, method, params }),
    });
    return parseSSE(await resp.text());
}

async function callTool(name: string, args: any = {}): Promise<string> {
    const resp = await mcpCall("tools/call", { name, arguments: args });
    const text = resp?.result?.content?.[0]?.text;
    assert.ok(text, `Tool ${name} returned no text content: ${JSON.stringify(resp)}\n${serverLogs}`);
    return text;
}

/** The version a read_note response hands back, from its `base_rev:` line. */
function baseRev(readText: string): string {
    const m = readText.match(/^base_rev: (\S+)$/m);
    assert.ok(m, `read_note gave no base_rev:\n${readText}`);
    return m[1];
}

/** The note body in a read_note response (after the `---` separator). */
function body(readText: string): string {
    const i = readText.indexOf("\n---\n\n");
    assert.ok(i >= 0, `read_note gave no body separator:\n${readText}`);
    return readText.slice(i + "\n---\n\n".length);
}

/** Two writers from the same base: the note ends up with two live leaves. */
async function makeConflict(notePath: string, a: string, b: string): Promise<void> {
    await callTool("write_note", { path: notePath, content: "base\n" });
    const rev0 = baseRev(await callTool("read_note", { path: notePath }));
    await callTool("write_note", { path: notePath, content: a, base_rev: rev0 });
    await callTool("write_note", { path: notePath, content: b, base_rev: rev0 });
    assert.equal((await leaves(notePath)).length, 2);
}

async function startServer(): Promise<void> {
    server = spawn(process.execPath, ["--import", "tsx", "src/main.ts"], {
        env: {
            ...process.env,
            PORT: String(PORT),
            HOST: "127.0.0.1",
            MCP_AUTH_TOKEN: AUTH,
            COUCHDB_URL: COUCH,
            COUCHDB_USER: COUCH_USER,
            COUCHDB_PASSWORD: COUCH_PASSWORD,
            COUCHDB_DATABASE: DB,
            DATA_DIR: dataDir,
            VAULT_NAME: "Ensaio",
        },
        stdio: "pipe",
    });
    server.stdout?.on("data", (d) => { serverLogs += d.toString(); });
    server.stderr?.on("data", (d) => { serverLogs += d.toString(); });

    const start = Date.now();
    while (Date.now() - start < 60000) {
        try {
            const resp = await fetch(BASE, {
                method: "POST",
                headers: { "Content-Type": "application/json", "Accept": "application/json, text/event-stream", "Authorization": `Bearer ${AUTH}` },
                body: JSON.stringify({ jsonrpc: "2.0", id: 0, method: "initialize", params: { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "versao-e2e", version: "1.0" } } }),
            });
            if (resp.ok) {
                sessionId = resp.headers.get("mcp-session-id") ?? "";
                return;
            }
        } catch { /* not ready */ }
        if (server.exitCode !== null) throw new Error(`server exited:\n${serverLogs}`);
        await new Promise((r) => setTimeout(r, 300));
    }
    throw new Error(`server did not start in time:\n${serverLogs}`);
}

describe("E2E (CouchDB): writes carry the version read", { skip: !COUCH && "HUB_TESTE_COUCHDB_URL not set" }, () => {
    before(async () => {
        const created = await couch("PUT", DB);
        assert.ok(created.ok, `could not create ${DB}: ${JSON.stringify(created)}`);
        dataDir = await mkdtemp(join(tmpdir(), "versao-e2e-"));
        await startServer();
    });

    after(async () => {
        if (process.env.HUB_TESTE_LOGS) console.log(`--- server logs ---\n${serverLogs}`);
        server?.kill();
        await new Promise((r) => setTimeout(r, 1000));
        await couch("DELETE", DB).catch(() => {});
        if (dataDir) await rm(dataDir, { recursive: true, force: true });
    });

    it("SONDA Fiel: duas gravações ao mesmo tempo da mesma base", async () => {
        const p = "iniciativas/alfa/simultanea.md";
        await callTool("write_note", { path: p, content: "base\n" });
        const rev0 = baseRev(await callTool("read_note", { path: p }));
        const call = async (content: string, id: number) => {
            const resp = await mcpCall("tools/call", { name: "write_note", arguments: { path: p, content, base_rev: rev0 } }, id);
            return resp?.result?.content?.[0]?.text ?? JSON.stringify(resp);
        };
        const [a, b] = await Promise.all([call("do escritor A\n", 101), call("do escritor B\n", 102)]);
        console.log("SONDA A =>", a.split("\n").slice(0, 3).join(" | "));
        console.log("SONDA B =>", b.split("\n").slice(0, 3).join(" | "));
        console.log("SONDA folhas =>", (await leafTexts(p)).length);
    });

    it("SONDA Fiel: recriar nota apagada sem base", async () => {
        const p = "iniciativas/alfa/apagada.md";
        await callTool("write_note", { path: p, content: "v1\n" });
        const rev = baseRev(await callTool("read_note", { path: p }));
        console.log("SONDA apagar =>", (await callTool("delete_note", { path: p, base_rev: rev })).split("\n")[0]);
        console.log("SONDA ler apagada =>", (await callTool("read_note", { path: p })).split("\n")[0]);
        console.log("SONDA recriar =>", (await callTool("write_note", { path: p, content: "v2\n" })).split("\n")[0]);
        console.log("SONDA ler =>", (await callTool("read_note", { path: p })).split("\n").slice(0, 4).join(" | "));
    });
});
