import math
import random

from merge_sort import merge_sort


def pior_caso(lista):
    if len(lista) <= 1:
        return lista
    return pior_caso(lista[0::2]) + pior_caso(lista[1::2])


def mostrar(nome, entrada):
    _, estatisticas = merge_sort(entrada)
    print(
        f"  {nome:<7} {estatisticas.comparacoes:>6} comparações   "
        f"{estatisticas.movimentacoes:>6} movimentações"
    )


print("Entrada do pior caso para n = 8:", pior_caso(list(range(1, 9))))

for n in (8, 64, 1024):
    log = int(math.log2(n))
    ordenada = list(range(n))
    print()
    print(f"n = {n}")
    mostrar("melhor", ordenada)
    mostrar("médio", random.Random(7).sample(ordenada, n))
    mostrar("pior", pior_caso(ordenada))
    print(
        f"  fórmulas: melhor = (n/2)·log2(n) = {n // 2 * log}   "
        f"pior = n·log2(n) - n + 1 = {n * log - n + 1}"
    )
