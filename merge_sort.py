"""Merge Sort estável, com contagem das operações de intercalação."""

from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")


@dataclass
class Estatisticas:
    comparacoes: int = 0
    movimentacoes: int = 0


def merge_sort(
    itens: list[T],
    *,
    chave: Callable[[T], object] = lambda item: item,
    trace: list[tuple] | None = None,
) -> tuple[list[T], Estatisticas]:
    """Retorna uma nova lista ordenada e os contadores, sem alterar a entrada.

    Uma comparação é uma avaliação entre as chaves de duas metades.
    Uma movimentação é a inserção de um elemento no resultado de uma
    intercalação, inclusive ao consumir a sobra de uma metade. Cópias de
    fatias não entram no contador. Empates favorecem a metade esquerda.
    """
    estatisticas = Estatisticas()

    def ordenar(lista: list[T], nivel: int = 0) -> list[T]:
        if len(lista) <= 1:
            return lista.copy()
        meio = len(lista) // 2
        if trace is not None:
            trace.append(("dividir", nivel, lista.copy()))
        esquerda = ordenar(lista[:meio], nivel + 1)
        direita = ordenar(lista[meio:], nivel + 1)
        resultado = []
        i = j = 0
        while i < len(esquerda) and j < len(direita):
            estatisticas.comparacoes += 1
            if chave(direita[j]) < chave(esquerda[i]):
                resultado.append(direita[j])
                j += 1
            else:
                resultado.append(esquerda[i])
                i += 1
            estatisticas.movimentacoes += 1
        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        estatisticas.movimentacoes += len(esquerda) - i + len(direita) - j
        if trace is not None:
            trace.append(
                ("intercalar", nivel, esquerda.copy(), direita.copy(), resultado.copy())
            )
        return resultado

    return ordenar(itens), estatisticas
