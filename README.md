# Jogo da Onça — Minimax com Poda Alfa-Beta (INFO7017/UFPR)

Implementação do Jogo da Onça com um agente de decisão baseado no algoritmo Minimax com poda Alfa-Beta, seguindo as especificações do arquivo trabalho.txt da disciplina INFO7017 — Inteligência Artificial (Mestrado em Informática/UFPR).

## Objetivo
- Modelar o Jogo da Onça como um problema de busca adversária.
- Implementar a decisão de jogadas com Minimax e poda Alfa-Beta.
- Separar a solução em módulos: estado do jogo, mecanismo de busca, modelagem/geração de ações e função de avaliação (quando aplicável).
- Permitir interação via comandos textuais de jogadas conforme o padrão do trabalho.

## Visão Geral do Jogo
- Tabuleiro: 7 linhas x 5 colunas, com 31 posições válidas.
- Peças: 1 onça (o) vs 14 cães (c).
- Condições de vitória:
  - Onça vence ao capturar 5 cães.
  - Cães vencem ao imobilizar a onça.
- Turnos: a onça sempre inicia.
- Movimentos:
  - Cães: movimentação simples para posições adjacentes válidas e livres.
  - Onça: pode mover como os cães ou realizar saltos (capturas) encadeados sobre cães adjacentes, desde que a posição imediatamente após o cão (na mesma direção) esteja livre. O salto não é obrigatório.

## Formato das Ações (I/O textual)
- Movimento simples:
  - `<peça> m <lin_orig> <col_orig> <lin_dest> <col_dest>`
  - Ex.: `c m 3 5 4 4`
- Salto da onça (n saltos em sequência):
  - `o s <n> <lin_orig> <col_orig> <seq_destinos>`
  - Ex.: `o s 3 5 3 3 5 3 3 3 1`

## Estrutura do Projeto
- Módulo do jogo: estado do tabuleiro, validação de movimentos e aplicação de jogadas.
- Módulo de movimentos: representação/parsing de ações.
- Módulo de busca (Minimax + Alfa-Beta): geração de sucessores, avaliação e escolha da melhor ação.
- Script de execução/demonstração.

## Requisitos
- Python 3.12.7
- Gerenciador de ambiente: virtualenv
- Pacotes instalados: pip

## Como executar
1) Crie e ative o ambiente virtual:
- Linux/macOS:
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`
- Windows (PowerShell):
  - `python -m venv .venv`
  - `.venv\Scripts\Activate.ps1`

2) Rode o script de demonstração:
- `python script.py`

3) Integração com jogador adversário:
- Leia e escreva ações no formato textual acima, turno a turno, usando o módulo do jogo para validar/aplicar as jogadas e o módulo de busca para decidir a próxima ação.

## Roadmap
- Implementar/ajustar:
  - Função de utilidade/avaliação (ex.: mobilidade da onça, número de cães capturados, risco de imobilização).
  - Geração completa de ações legais para ambos os lados.
  - Minimax com poda Alfa-Beta e profundidade configurável.
  - Interface de I/O (stdin/stdout) para torneio/avaliação automática.
- Testes:
  - Casos unitários de validação de movimentos e saltos.
  - Cenários de meio de jogo para avaliação heurística.
  - Stress tests de desempenho/tempo por jogada.

## Licença
Defina uma licença apropriada para o trabalho (por exemplo, MIT), conforme necessidade do repositório.

## Referências
- Especificação do trabalho (trabalho.txt).
- Jogo da Onça: https://pt.wikipedia.org/wiki/Jogo_da_onça
