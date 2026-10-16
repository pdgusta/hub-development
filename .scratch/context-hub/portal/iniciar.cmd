@echo off
rem Sobe o portal a partir desta pasta e abre a pagina no navegador padrao (proposta, secao 5.2).
rem Por duplo clique (fora do canvas): tudo funciona, o aviso ao agente fica indisponivel e a pagina avisa.
rem Pelo terminal do canvas: herda MAESTRI_PIPE e MAESTRI_TERMINAL_ID e o aviso fica ativo.
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python 3.12 ou mais novo nao encontrado no PATH.
  pause
  exit /b 1
)
rem A porta vem do projeto.json: o servidor imprime a URL e abre o navegador quando a porta esta aberta.
python nucleo\torre.py projeto.json --abrir
if errorlevel 1 pause
endlocal
