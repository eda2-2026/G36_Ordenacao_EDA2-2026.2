import csv
import math
import subprocess
import sys

import pytest

from benchmark import CENARIOS, executar, resumir, escrever_csv
from casos import pior_caso
from merge_sort import merge_sort


@pytest.mark.parametrize('n', [2, 4, 8, 32, 128])
def test_limites_teoricos(n):
    ordenada = list(range(n))
    entrada = pior_caso(ordenada)
    resultado, pior = merge_sort(entrada)
    melhor = merge_sort(ordenada)[1]
    log = int(math.log2(n))
    assert resultado == ordenada
    assert melhor.comparacoes == n // 2 * log
    assert pior.comparacoes == n * log - n + 1
    assert pior.movimentacoes == melhor.movimentacoes == n * log


def test_benchmark_reprodutivel_e_csv(tmp_path):
    medicoes = executar([8, 16], amostras=2, repeticoes=2, semente=7)
    outra = executar([8, 16], amostras=2, repeticoes=2, semente=7)
    assert len(medicoes) == 24
    assert [{k: v for k, v in m.items() if k != 'tempo_ms'} for m in medicoes] == [
        {k: v for k, v in m.items() if k != 'tempo_ms'} for m in outra
    ]
    assert all(m['tempo_ms'] >= 0 for m in medicoes)
    resumo = resumir(medicoes)
    assert len(resumo) == 6
    assert {r['cenario'] for r in resumo} == set(CENARIOS)
    assert all(r['medicoes'] == 4 for r in resumo)
    caminho = tmp_path / 'resumo.csv'
    escrever_csv(caminho, resumo)
    with caminho.open() as arquivo:
        assert len(list(csv.DictReader(arquivo))) == 6


def test_resumo_estatistico():
    medicoes = [dict(n=8, cenario=c, tempo_ms=t, comparacoes=12, movimentacoes=24)
                for c in CENARIOS for t in (1, 2, 6)]
    for linha in resumir(medicoes):
        assert linha['tempo_medio_ms'] == 3
        assert linha['tempo_mediano_ms'] == 2
        assert linha['desvio_padrao_ms'] == pytest.approx(math.sqrt(7))


@pytest.mark.parametrize('tamanhos,amostras,repeticoes', [([], 1, 1), ([1], 1, 1), ([8], 0, 1), ([8], 1, 0)])
def test_parametros_invalidos(tamanhos, amostras, repeticoes):
    with pytest.raises(ValueError):
        executar(tamanhos, amostras, repeticoes)


def test_importar_casos_nao_executa_experimento():
    resultado = subprocess.run([sys.executable, '-c', 'import casos'], capture_output=True, text=True, check=True)
    assert resultado.stdout == ''
