#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"
REQUIREMENTS_FILE="${SCRIPT_DIR}/requirements.txt"
PYTHON_BIN="${PYTHON_BIN:-python3}"
OLLAMA_MODEL="${OLLAMA_MODEL:-mistral:latest}"

echo "=================================================="
echo "[setup] Iniciando setup do projeto"
echo "=================================================="
echo "[setup] Diretório do projeto: ${SCRIPT_DIR}"
echo "[setup] Python selecionado: ${PYTHON_BIN}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "[erro] Python não encontrado: ${PYTHON_BIN}"
  echo "[dica] Instale Python 3 e tente novamente."
  exit 1
fi

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "[setup] Criando ambiente virtual em ${VENV_DIR}..."
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
else
  echo "[setup] Ambiente virtual já existe em ${VENV_DIR}."
fi

echo "[setup] Ativando ambiente virtual..."
# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"

if [[ ! -f "${REQUIREMENTS_FILE}" ]]; then
  echo "[erro] Arquivo de dependências não encontrado: ${REQUIREMENTS_FILE}"
  exit 1
fi

echo "[setup] Atualizando ferramentas base do pip..."
python -m pip install --upgrade pip setuptools wheel

echo "[setup] Instalando dependências Python do projeto..."
echo "[setup] Usando arquivo: ${REQUIREMENTS_FILE}"
python -m pip install -r "${REQUIREMENTS_FILE}"

echo "[setup] Verificando instalação do Ollama CLI..."
if ! command -v ollama >/dev/null 2>&1; then
  echo "[erro] Ollama não está instalado no sistema."
  echo "[dica] Instale com: curl -fsSL https://ollama.com/install.sh | sh"
  exit 1
fi

echo "[setup] Verificando conexão com serviço Ollama..."
if ! ollama list >/dev/null 2>&1; then
  echo "[erro] Serviço Ollama indisponível."
  echo "[dica] Inicie o Ollama (ex.: 'ollama serve') e execute o setup novamente."
  exit 1
fi

echo "[setup] Baixando modelo ${OLLAMA_MODEL} (se necessário)..."
ollama pull "${OLLAMA_MODEL}"

echo "=================================================="
echo "[setup] Setup concluído com sucesso."
echo "[setup] Para executar o projeto:"
echo "        source .venv/bin/activate && python main.py"
echo "=================================================="
