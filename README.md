# QA Pipeline

Este projeto roda uma pipeline de inferência QA em dados `.parquet`, exportando o resultado final para CSV e usando o modelo local `mistral:latest` via Ollama.
- O `parquet` utilizado estará incluso em `./input/` e nenhum download é necessário

## 1) Pré-requisitos

Antes de executar, garanta que seu sistema tenha:

- `python3` (recomendado: 3.10+)
- `venv` (normalmente vem com Python)
- [Ollama](https://ollama.com/download) instalado
- Serviço do Ollama em execução (`ollama serve`, caso necessário)
- No Windows, verifique se o Ollama foi adicionado ao path
- Em caso de execução do setup antes da instalação do Ollama, o erro: "[erro] Ollama não está instalado no sistema." será mostrado. Instale, certifique-se que o Ollama consta no PATH e execute o `setup` novamente para terminar a instalação do modelo.

## 2) Setup automático

Foram criados os scripts `setup.sh` (Linux/macOS) e `setup.ps1` (Windows), que fazem automaticamente:

1. Criação de ambiente virtual em `.venv`
2. Ativação do ambiente virtual
3. Upgrade de `pip`, `setuptools` e `wheel`
4. Instalação das dependências Python do projeto via `requirements.txt`
5. Verificação do Ollama
6. Download do modelo `mistral:latest`

### Comando (Linux/macOS)

```bash
./setup.sh
```

### Comando (Windows / PowerShell)

```powershell
.\setup.ps1
```

## 3) Executar o pipeline

Após setup concluído. Da raíz do projeto:

### Linux/macOS

```bash
source .venv/bin/activate
python main.py
```

### Windows / PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

## 4) Saídas esperadas

- CSV final em `output/results_complete.csv`
- Arquivos temporários de checkpoint/timeout em `temp/` durante a execução

Ao final do `run()`, os arquivos temporários são limpos pelo próprio fluxo.

## 5) Execução em um único comando

Se quiser fazer setup + execução diretamente.

### Linux/macOS

```bash
./setup.sh && source .venv/bin/activate && python main.py
```

### Windows / PowerShell

```powershell
.\setup.ps1; .\.venv\Scripts\Activate.ps1; python main.py
```

## 6) Solução de problemas

- **`python3: command not found` / `python: command not found`**
  - Instale Python 3 no sistema.
- **`Ollama não está instalado`**
  - Instale com:
    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    ```
- **`Serviço Ollama indisponível`**
  - Inicie com:
    ```bash
    ollama serve
    ```
  - Em outro terminal, rode novamente `./setup.sh` ou `.\setup.ps1`.
- **Erro ao baixar modelo**
  - Verifique conexão de internet e tente:
    ```bash
    ollama pull mistral:latest
    ```
- **Windows bloqueia execução de script PowerShell**
  - Rode uma vez no PowerShell (usuário atual):
    ```powershell
    Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
    ```

## 7) Estrutura de execução (resumo)

- Entrada padrão: `input/0000.parquet`
- Script principal: `main.py`
- Orquestração: `orchestrator.py`
- Saída padrão: `output/results_complete.csv`
