import random

import pytest

from merge_sort import Estatisticas, merge_sort


@pytest.mark.parametrize("entrada", [[], [7], [1, 2, 3], [3, 2, 1], [4, 4, 4], [0, -2, 7, -2]])
def test_ordena_sem_modificar_entrada(entrada):
    original = entrada.copy()
    resultado, _ = merge_sort(entrada)
    assert resultado == sorted(original)
    assert entrada == original
    assert resultado is not entrada


def test_estabilidade_com_chaves_iguais():
    entrada = [(2, "A"), (1, "B"), (2, "C"), (1, "D"), (2, "E")]
    resultado, _ = merge_sort(entrada, chave=lambda item: item[0])
    assert resultado == [(1, "B"), (1, "D"), (2, "A"), (2, "C"), (2, "E")]


@pytest.mark.parametrize("entrada,comparacoes,movimentacoes", [
    ([], 0, 0), ([1], 0, 0), ([2, 1], 1, 2),
    ([1, 2, 3, 4], 4, 8), ([1, 3, 2, 4], 5, 8),
])
def test_contadores(entrada, comparacoes, movimentacoes):
    _, estatisticas = merge_sort(entrada)
    assert estatisticas == Estatisticas(comparacoes, movimentacoes)
    assert merge_sort([])[1] == Estatisticas()


def test_listas_aleatorias_com_repeticoes():
    gerador = random.Random(36)
    for tamanho in [3, 17, 64, 101, 1000]:
        entrada = [gerador.randint(-20, 20) for _ in range(tamanho)]
        resultado, _ = merge_sort(entrada)
        assert resultado == sorted(entrada)


def test_trace_registra_divisoes_e_intercalacoes_em_ordem():
    passos = []
    resultado, _ = merge_sort([3, 1, 2], trace=passos)
    assert resultado == [1, 2, 3]
    assert passos == [
        ("dividir", 0, [3, 1, 2]),
        ("dividir", 1, [1, 2]),
        ("intercalar", 1, [1], [2], [1, 2]),
        ("intercalar", 0, [3], [1, 2], [1, 2, 3]),
    ]


def test_trace_nao_altera_resultado_nem_contadores():
    entrada = [5, 3, 8, 3, 1, 9, 2]
    sem_trace = merge_sort(entrada)
    com_trace = merge_sort(entrada, trace=[])
    assert com_trace == sem_trace


@pytest.mark.parametrize("entrada", [[], [7]])
def test_trace_vazio_sem_divisoes(entrada):
    passos = []
    merge_sort(entrada, trace=passos)
    assert passos == []
