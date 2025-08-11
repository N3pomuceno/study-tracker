#!/bin/bash

# --- Funções Auxiliares ---

### Activates the Python venv, creating if necessary
### Parameters: none
###
activate_venv () {

    # Check if running on Windows or Linux/Mac
    if [ "${OS:-x}" == "Windows_NT" ]; then
        activate_path='Scripts/activate'
    else
        activate_path='bin/activate'
    fi

    # VENV directory
    venv_dir="$(pwd)/.venv"
    log "Venv directory: ${venv_dir}"

    # Check if the .venv folder exists
    if [ ! -d "${venv_dir}" ]; then
        log "Error: VENV not found at ${venv_dir}"
        exit 20
    else
        log "VENV found. Activating..."
        source "${venv_dir}"/${activate_path}
    fi
}

# Função para logar mensagens com timestamp
log () {
    local message="$1"
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $message"
}
