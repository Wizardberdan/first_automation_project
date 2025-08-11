@echo off
REM ========================================
REM Script para configurar tarefa agendada no Windows
REM Execute como Administrador
REM ========================================

echo Configurando tarefa agendada para o Sistema de Vendas...

REM Verificar se está rodando como administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Este script deve ser executado como Administrador
    echo Clique com o botão direito e selecione "Executar como administrador"
    pause
    exit /b 1
)

REM Obter o diretório atual
set CURRENT_DIR=%~dp0
set SCRIPT_PATH=%CURRENT_DIR%run_vendas.bat

REM Verificar se o script principal existe
if not exist "%SCRIPT_PATH%" (
    echo ERRO: Arquivo run_vendas.bat não encontrado em: %SCRIPT_PATH%
    pause
    exit /b 1
)

REM Configurações da tarefa
set TASK_NAME=Sistema-Vendas-Diario
set TASK_TIME=08:00
set TASK_USER=%USERNAME%

echo.
echo Configurações da tarefa:
echo Nome: %TASK_NAME%
echo Horário: %TASK_TIME% (diariamente)
echo Script: %SCRIPT_PATH%
echo Usuário: %TASK_USER%
echo.

REM Remover tarefa existente (se houver)
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

REM Criar nova tarefa agendada
schtasks /create /tn "%TASK_NAME%" /tr "\"%SCRIPT_PATH%\"" /sc daily /st %TASK_TIME% /ru "%TASK_USER%" /rl highest /f

if %errorlevel% equ 0 (
    echo.
    echo ✓ Tarefa agendada criada com SUCESSO!
    echo.
    echo A tarefa será executada diariamente às %TASK_TIME%
    echo.
    echo Para verificar: Abra o "Agendador de Tarefas" do Windows
    echo e procure por "%TASK_NAME%"
    echo.
    echo Para executar manualmente agora:
    echo schtasks /run /tn "%TASK_NAME%"
) else (
    echo.
    echo ✗ ERRO ao criar tarefa agendada
    echo Verifique as permissões e tente novamente
)

echo.
pause