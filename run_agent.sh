#!/bin/bash

# --- VARIAVEIS DE AMBIENTE ---
AGENT_SCRIPT="main_agent.py"
AGENT_SIDE=${1:-o} # Lado padrão é 'o' se não for especificado
DEPTH=${2:-5}     # Profundidade padrão é 5

echo "================================================="
echo "INICIANDO SETUP PARA AGENTE JOGO DA ONÇA"
echo "LADO: ${AGENT_SIDE} | PROFUNDIDADE: ${DEPTH}"
echo "================================================="

# --- 1. CONFIGURACAO DO AMBIENTE VIRTUAL PYTHON ---
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

echo "Ativando ambiente virtual..."
source venv/bin/activate

echo "Instalando dependências Python..."
pip install -r requirements.txt

# --- 4. EXECUÇÃO DO AGENTE ---
echo "EXECUTANDO AGENTE: python3 ${AGENT_SCRIPT} ${AGENT_SIDE} ${DEPTH}"
python3 "${AGENT_SCRIPT}" "${AGENT_SIDE}" "${DEPTH}"

deactivate # Desativa o ambiente virtual ao encerrar o script