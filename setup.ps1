#!/usr/bin/env pwsh

$ErrorActionPreference = "Stop"

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$VENV_DIR = Join-Path $SCRIPT_DIR ".venv"
$REQUIREMENTS_FILE = Join-Path $SCRIPT_DIR "requirements.txt"
$PYTHON_BIN = if ($env:PYTHON_BIN) { $env:PYTHON_BIN } else { "python" }
$OLLAMA_MODEL = if ($env:OLLAMA_MODEL) { $env:OLLAMA_MODEL } else { "mistral:latest" }

Write-Host "=================================================="
Write-Host "[setup] Iniciando setup do projeto"
Write-Host "=================================================="
Write-Host "[setup] Diretório do projeto: $SCRIPT_DIR"
Write-Host "[setup] Python selecionado: $PYTHON_BIN"

if (-not (Get-Command $PYTHON_BIN -ErrorAction SilentlyContinue)) {
    Write-Host "[erro] Python não encontrado: $PYTHON_BIN"
    Write-Host "[dica] Instale Python 3 e tente novamente."
    exit 1
}

if (-not (Test-Path $VENV_DIR -PathType Container)) {
    Write-Host "[setup] Criando ambiente virtual em $VENV_DIR..."
    & $PYTHON_BIN -m venv $VENV_DIR
}
else {
    Write-Host "[setup] Ambiente virtual já existe em $VENV_DIR."
}

$ACTIVATE_SCRIPT = Join-Path $VENV_DIR "Scripts\Activate.ps1"
if (-not (Test-Path $ACTIVATE_SCRIPT -PathType Leaf)) {
    Write-Host "[erro] Script de ativação não encontrado: $ACTIVATE_SCRIPT"
    exit 1
}

Write-Host "[setup] Ativando ambiente virtual..."
. $ACTIVATE_SCRIPT

if (-not (Test-Path $REQUIREMENTS_FILE -PathType Leaf)) {
    Write-Host "[erro] Arquivo de dependências não encontrado: $REQUIREMENTS_FILE"
    exit 1
}

Write-Host "[setup] Atualizando ferramentas base do pip..."
python -m pip install --upgrade pip setuptools wheel

Write-Host "[setup] Instalando dependências Python do projeto..."
Write-Host "[setup] Usando arquivo: $REQUIREMENTS_FILE"
python -m pip install -r $REQUIREMENTS_FILE

Write-Host "[setup] Verificando instalação do Ollama CLI..."
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "[erro] Ollama não está instalado no sistema."
    Write-Host "[dica] Instale em: https://ollama.com/download"
    Write-Host "[dica] Caso tenha instalado anteriormente, certifique-se que o Ollama foi adicionado ao PATH"
    Write-Host "[dica] Após instalar, execute este script novamente para concluir o setup e baixar o modelo $OLLAMA_MODEL."
    exit 1
}

Write-Host "[setup] Verificando conexão com serviço Ollama..."
try {
    ollama list | Out-Null
}
catch {
    Write-Host "[erro] Serviço Ollama indisponível."
    Write-Host "[dica] Inicie o Ollama e execute o setup novamente."
    exit 1
}

Write-Host "[setup] Baixando modelo $OLLAMA_MODEL (se necessário)..."
ollama pull $OLLAMA_MODEL

Write-Host "=================================================="
Write-Host "[setup] Setup concluído com sucesso."
Write-Host "[setup] Para executar o projeto:"
Write-Host "        .\.venv\Scripts\Activate.ps1; python main.py"
Write-Host "=================================================="
