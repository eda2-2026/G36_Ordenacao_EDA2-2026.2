# G36_Ordenacao_EDA2 - FilaChamados

Sistema de linha de comando (CLI) em Python para uma fila de chamados de suporte técnico,
ordenada por prioridade e horário de chegada com o algoritmo Merge Sort.

O objetivo do trabalho é aplicar os algoritmos de ordenação estudados em EDA2,
implementando o Merge Sort e analisando sua complexidade, sua estabilidade e seu
desempenho conforme a quantidade de chamados cresce.

## Entrega parcial — aproximadamente 40%

O percentual é uma estimativa de escopo, dividida em cinco etapas; não representa
uma medição de horas nem um critério de avaliação da disciplina.

| Etapa | Estado |
| ----- | ------ |
| 1. Merge Sort estável, contadores e testes do algoritmo | Concluída |
| 2. Modelo, validações, fila, CSV e testes de integração | Concluída |
| 3. CLI e visualização passo a passo | Pendente |
| 4. Análise de melhor, médio e pior caso | Pendente |
| 5. Benchmark, gráficos e conclusão da documentação/apresentação | Pendente |

A descrição abaixo apresenta o sistema planejado. Nesta entrega, o núcleo funciona
por chamadas Python; o menu interativo ainda não foi implementado.

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
```

Exemplo executável do núcleo atual, a partir da pasta do projeto:

```bash
python - <<'PY'
from atendimento import FilaAtendimento

fila = FilaAtendimento()
fila.carregar_csv("chamados.csv")
fila.registrar("Fernanda", "Sistema indisponível", 1, "08:50")
chamados, estatisticas = fila.listar_ordenados()
for chamado in chamados:
    print(chamado)
print(estatisticas)
atendido, estatisticas = fila.atender_proximo()
print("Atendido:", atendido)
print("Operações do atendimento:", estatisticas)
fila.salvar_csv("/tmp/filachamados-exemplo.csv")
PY
```

Os horários devem estar em `HH:MM` e são considerados dentro de um mesmo dia.
Prioridades aceitas: inteiros de 1 a 4. Cliente e descrição não podem ser vazios.
O CSV usa UTF-8 e cabeçalho `cliente,descricao,prioridade,horario`; preserva a
ordem de registro para desempates. Carregar substitui a fila apenas após validar
todo o arquivo. Arquivo ausente gera `FileNotFoundError`; formato inválido gera
`ValueError`. Registrar e atender só alteram a memória: use `salvar_csv` para persistir.

`merge_sort` e `listar_ordenados` retornam `(lista, estatisticas)`;
`atender_proximo` retorna `(chamado, estatisticas)`, com `None` na fila vazia.
As comparações contam avaliações de chaves entre metades; as movimentações contam
cada inserção no resultado das intercalações, incluindo sobras. Cópias de fatias
não entram nessa contagem. Os contadores reiniciam a cada ordenação.

Testes automatizados:

```bash
python -m pytest
```

Comandos previstos para as próximas etapas (arquivos ainda não implementados):

```bash
python main.py
python casos.py
python benchmark.py
```

## Estrutura do projeto

```
main.py            CLI com menu interativo (pendente)
merge_sort.py      Merge Sort com contadores de comparações e movimentações
atendimento.py     chamado, validações, fila de atendimento e CSV
casos.py           melhor, médio e pior caso do Merge Sort (pendente)
benchmark.py       experimento de desempenho e gráficos (pendente)
chamados.csv       base de exemplo
test_*.py          testes automatizados
resultados/        gráficos gerados pelo benchmark (pendente)
```
