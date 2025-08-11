@echo off
REM ========================================
REM Script para execução automatizada do sistema de vendas
REM Executa o container Docker e salva logs
REM ========================================

REM Configurações
set CONTAINER_NAME=sistema-vendas
set SCRIPT_PATH=/app/toFornecedor.py
set LOG_DIR=%~dp0logs
set LOGFILE=%LOG_DIR%\vendas_%date:~6,4%-%date:~3,2%-%date:~0,2%.log

REM Criar diretório de logs se não existir
if not exist "%LOG_DIR%" (
    mkdir "%LOG_DIR%"
)

REM Adicionar timestamp no início da execução
echo. >> "%LOGFILE%"
echo ========================================== >> "%LOGFILE%"
echo [%date% %time%] Iniciando execução do sistema de vendas >> "%LOGFILE%"
echo ========================================== >> "%LOGFILE%"

REM Verificar se o container está rodando
docker ps --filter "name=%CONTAINER_NAME%" --format "table {{.Names}}" | findstr /C:"%CONTAINER_NAME%" >nul
if %errorlevel% neq 0 (
    echo [%date% %time%] ERRO: Container %CONTAINER_NAME% não está rodando >> "%LOGFILE%"
    echo [%date% %time%] Tentando iniciar o container... >> "%LOGFILE%"
    docker start %CONTAINER_NAME% >> "%LOGFILE%" 2>&1
    if %errorlevel% neq 0 (
        echo [%date% %time%] ERRO: Falha ao iniciar o container >> "%LOGFILE%"
        exit /b 1
    )
    echo [%date% %time%] Container iniciado com sucesso >> "%LOGFILE%"
)

REM Executar o script Python no container
echo [%date% %time%] Executando script de extração de vendas... >> "%LOGFILE%"
docker exec %CONTAINER_NAME% python %SCRIPT_PATH% >> "%LOGFILE%" 2>&1

REM Verificar o resultado da execução
if %errorlevel% equ 0 (
    echo [%date% %time%] Execução concluída com SUCESSO >> "%LOGFILE%"
) else (
    echo [%date% %time%] Execução FALHOU - Código de erro: %errorlevel% >> "%LOGFILE%"
)

echo ========================================== >> "%LOGFILE%"
echo [%date% %time%] Fim da execução >> "%LOGFILE%"
echo ========================================== >> "%LOGFILE%"

REM Manter apenas os últimos 30 dias de logs (opcional - descomente se necessário)
REM forfiles /p "%LOG_DIR%" /m "vendas_*.log" /d -30 /c "cmd /c del @path" 2>nul

exit /b %errorlevel%