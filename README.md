# G36_Ordenacao_EDA2 - FilaChamados

Sistema de linha de comando (CLI) em Python para uma fila de chamados de suporte técnico,
ordenada por prioridade e horário de chegada com o algoritmo Merge Sort.

O objetivo do trabalho é aplicar os algoritmos de ordenação estudados em EDA2,
implementando o Merge Sort e analisando sua complexidade, sua estabilidade e seu
desempenho conforme a quantidade de chamados cresce.

## Vídeo de apresentação

Link a ser adicionado.

## Alunos

| Matrícula | Nome                           |
| --------- | ------------------------------ |
| 231011328 | Felipe de Aquino Campelo       |
| 232000688 | Arthur Palhares Ferreira Silva |

## Descrição

O sistema gerencia chamados de atendimento (cliente, descrição, prioridade e horário de
chegada). A prioridade vai de 1 (crítica) a 4 (baixa) e o horário é informado no formato
HH:MM. A fila é sempre apresentada ordenada por prioridade e, em caso de empate, pelo
horário de chegada, de forma que o próximo chamado a ser atendido é o primeiro da fila.

É possível registrar chamados, ver a fila ordenada, atender o próximo e acompanhar o
Merge Sort passo a passo. Os dados são persistidos em arquivo CSV.

## Algoritmo de ordenação

- Merge Sort: algoritmo de divisão e conquista que divide a lista ao meio, ordena cada
  metade recursivamente e intercala as duas metades já ordenadas.
- Estável: chamados com a mesma prioridade e o mesmo horário mantêm a ordem em que foram
  registrados, o que é essencial para uma fila justa.
- Complexidade: Θ(n log n) em tempo no melhor, médio e pior caso; O(n) de espaço auxiliar.
- Cada ordenação informa o número de comparações e de movimentações realizadas.

## Como executar

Requisitos: Python 3.11+.

```bash
pip install -r requirements.txt
python main.py
```

Testes automatizados:

```bash
pytest
```

Análise de melhor, médio e pior caso e experimento de desempenho:

```bash
python casos.py
python benchmark.py
```

## Estrutura do projeto

```
main.py            CLI com menu interativo
merge_sort.py      Merge Sort com contadores de comparações e movimentações
atendimento.py     chamado, validações, fila de atendimento e CSV
casos.py           melhor, médio e pior caso do Merge Sort
benchmark.py       experimento de desempenho e gráficos
chamados.csv       base de exemplo
test_*.py          testes automatizados
resultados/        gráficos gerados pelo benchmark
```
