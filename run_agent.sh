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

# --- 2. COMPILACAO DO CONTROLADOR C ---
echo "Compilando programas C (controlador, exemplos)..."
# Assumindo que o makefile e os arquivos C estão no diretório atual
make clean # Limpa binários anteriores
make       # Compila os novos binários

# --- 3. INSTRUÇÕES PARA O USUÁRIO ---
echo "================================================="
echo "SETUP COMPLETO! PRONTO PARA CONECTAR NO REDIS:10001"
echo "================================================="
echo ">> ANTES DE INICIAR O AGENTE, VOCÊ DEVE RODAR:"
echo ">> 1) O SERVIDOR REDIS: redis-server redis.conf"
echo ">> 2) O CONTROLADOR: ./controlador ${AGENT_SIDE} 50 0"
echo "-------------------------------------------------"
echo "INICIANDO SEU AGENTE EM 5 SEGUNDOS..."
sleep 5

# --- 4. EXECUÇÃO DO AGENTE ---
echo "EXECUTANDO AGENTE: python3 ${AGENT_SCRIPT} ${AGENT_SIDE} ${DEPTH}"
python3 "${AGENT_SCRIPT}" "${AGENT_SIDE}" "${DEPTH}"

deactivate # Desativa o ambiente virtual ao encerrar o script