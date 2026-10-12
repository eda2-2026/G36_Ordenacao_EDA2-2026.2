"""Contagens teóricas para chaves distintas e tamanhos potência de dois."""

import math
import random
from statistics import mean

from merge_sort import merge_sort


def pior_caso(lista):
    """Recebe chaves distintas ordenadas; uso demonstrado com potências de dois."""
    if len(lista) <= 1:
        return lista
    return pior_caso(lista[0::2]) + pior_caso(lista[1::2])


def mostrar(nome, estatisticas):
    print(
        f"  {nome:<7} {mean(e.comparacoes for e in estatisticas):>9.2f} comparações   "
        f"{mean(e.movimentacoes for e in estatisticas):>9.2f} movimentações"
    )


def main():
    gerador = random.Random(7)
    print("Entrada do pior caso para n = 8:", pior_caso(list(range(1, 9))))
    print("Médio: média de 30 permutações aleatórias por tamanho (semente 7).")
    print("Fórmulas abaixo: chaves distintas e n potência de dois.")
    for n in (8, 64, 1024):
        log = int(math.log2(n))
        ordenada = list(range(n))
        print(f"\nn = {n}")
        mostrar("melhor", [merge_sort(ordenada)[1]])
        mostrar("médio", [merge_sort(gerador.sample(ordenada, n))[1] for _ in range(30)])
        mostrar("pior", [merge_sort(pior_caso(ordenada))[1]])
        print(
            f"  fórmulas: melhor = (n/2)·log2(n) = {n // 2 * log}   "
            f"pior = n·log2(n) - n + 1 = {n * log - n + 1}"
        )
    print("\nTodos os casos: Θ(n log n) em tempo e O(n) de espaço auxiliar sem trace.")
    print("Uma entrada invertida não é, em geral, o pior caso do Merge Sort.")


if __name__ == "__main__":
    main()
