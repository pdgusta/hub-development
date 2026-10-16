@echo off
rem Painel da construcao: sobe o servidor (so leitura, 127.0.0.1:8771) e abre o navegador.
rem   iniciar.cmd             le ..\execucao\
rem   iniciar.cmd --fixture   le fixture\execucao-fake\ (rode antes: node fixture\gerar.mjs)
rem Ctrl+C nesta janela desliga o painel. A execucao nao depende dele.
cd /d "%~dp0"
start "" cmd /c "timeout /t 2 /nobreak >nul & start "" http://127.0.0.1:8771/"
python servidor.py %*
