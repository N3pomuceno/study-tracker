#!/bin/bash

# Configuration to make the script fail on errors or undefined variables
set -eu -o pipefail

source "src/exec-functions.sh"

# Função para verificar se um comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# --- Configuração de Logs ---

LOGS_DIR="./logs"
mkdir -p "$LOGS_DIR"
LOG_FILE="${LOGS_DIR}/execution-$(date +"%Y-%m-%d_%H-%M-%S").log"

# Redireciona toda a saída (stdout e stderr) para o log e para o terminal
exec > >(tee -a "$LOG_FILE") 2>&1

# --- Início da Execução ---

log "Iniciando o script de setup..."
log "Activating Python virtual environment..."
activate_venv

# 1. Verificar dependências
log "Verificando dependências necessárias..."
if ! command_exists docker compose; then
    log "ERRO: docker compose não encontrado. Por favor, instale-o para continuar."
    exit 1
fi
if ! command_exists python3; then
    log "ERRO: python3 não encontrado. Por favor, instale-o para continuar."
    exit 1
fi
log "Dependências encontradas."

# 2. Subir os contêineres
log "Iniciando os contêineres com Docker Compose..."
docker compose up -d

# 3. Aguardar o banco de dados ficar pronto
log "Aguardando o serviço de banco de dados ficar pronto... (tentativas por 30s)"
WAIT_COMMAND="while ! nc -z localhost 5433; do sleep 1; done"
timeout 30s bash -c "$WAIT_COMMAND" || (log "ERRO: Banco de dados não ficou disponível a tempo." && docker-compose down && exit 1)
log "Banco de dados está pronto para aceitar conexões."

# 4. Rodar o script de setup do banco
log "Executando o script de configuração do banco de dados..."
python3 src/db_creation.py
log "Configuração do banco de dados concluída."

# 5. Desligar os contêineres
log "Parando os contêineres..."
docker compose down

log "Script finalizado com sucesso."
