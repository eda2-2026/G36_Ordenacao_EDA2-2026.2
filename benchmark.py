"""Experimento reproduzível de ordenação de chamados, sem trace ou I/O cronometrado."""

import argparse
import csv
import json
import platform
import random
from pathlib import Path
from statistics import mean, median, stdev
from time import perf_counter_ns

from atendimento import Chamado
from merge_sort import merge_sort

CENARIOS = ("ordenado", "aleatorio", "inverso")


def chave(chamado):
    return chamado.prioridade, chamado.horario


def gerar_chamados(n, gerador):
    chamados = []
    for i in range(n):
        minuto = gerador.randrange(1440)
        chamados.append(Chamado(
            f"Cliente {i}", "Solicitação de suporte", gerador.randint(1, 4),
            f"{minuto // 60:02d}:{minuto % 60:02d}",
        ))
    return chamados


def executar(tamanhos, amostras=5, repeticoes=3, semente=36):
    if not tamanhos or any(n < 2 for n in tamanhos):
        raise ValueError("Informe tamanhos maiores ou iguais a 2.")
    if amostras < 1 or repeticoes < 1:
        raise ValueError("Amostras e repetições devem ser positivas.")
    gerador = random.Random(semente)
    medicoes = []
    for n in tamanhos:
        for amostra in range(1, amostras + 1):
            base = gerar_chamados(n, gerador)
            entradas = {
                "ordenado": sorted(base, key=chave),
                "aleatorio": base,
                "inverso": sorted(base, key=chave, reverse=True),
            }
            # Aquecimento fora da medição, para cada cenário e amostra.
            for entrada in entradas.values():
                merge_sort(entrada, chave=chave)
            for repeticao in range(1, repeticoes + 1):
                ordem = list(CENARIOS)
                gerador.shuffle(ordem)
                for cenario in ordem:
                    entrada = entradas[cenario]
                    inicio = perf_counter_ns()
                    resultado, estatisticas = merge_sort(entrada, chave=chave)
                    tempo_ms = (perf_counter_ns() - inicio) / 1_000_000
                    # sorted é somente referência de correção, fora do cronômetro.
                    if resultado != sorted(entrada, key=chave):
                        raise AssertionError("Resultado incorreto ou instável.")
                    medicoes.append(dict(
                        n=n, cenario=cenario, amostra=amostra, repeticao=repeticao,
                        tempo_ms=tempo_ms, comparacoes=estatisticas.comparacoes,
                        movimentacoes=estatisticas.movimentacoes,
                    ))
    return medicoes


def resumir(medicoes):
    resumo = []
    for n in sorted({m["n"] for m in medicoes}):
        for cenario in CENARIOS:
            grupo = [m for m in medicoes if m["n"] == n and m["cenario"] == cenario]
            tempos = [m["tempo_ms"] for m in grupo]
            resumo.append(dict(
                n=n, cenario=cenario, medicoes=len(grupo),
                tempo_medio_ms=mean(tempos), tempo_mediano_ms=median(tempos),
                desvio_padrao_ms=stdev(tempos) if len(tempos) > 1 else 0.0,
                comparacoes_medias=mean(m["comparacoes"] for m in grupo),
                movimentacoes_medias=mean(m["movimentacoes"] for m in grupo),
            ))
    return resumo


def escrever_csv(caminho, linhas):
    with caminho.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
        escritor.writeheader()
        escritor.writerows(linhas)


def gerar_graficos(resumo, pasta):
    import math
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    for campo, nome, titulo, unidade in [
        ("tempo_mediano_ms", "tempos.png", "Tempo de ordenação de chamados", "Tempo mediano (ms)"),
        ("comparacoes_medias", "comparacoes.png", "Comparações por tamanho da fila", "Comparações médias"),
        ("movimentacoes_medias", "movimentacoes.png", "Movimentações por tamanho da fila", "Movimentações médias"),
    ]:
        fig, ax = plt.subplots(figsize=(9, 5), constrained_layout=True)
        for cenario in CENARIOS:
            grupo = [r for r in resumo if r["cenario"] == cenario]
            ax.plot([r["n"] for r in grupo], [r[campo] for r in grupo], marker="o", label=cenario)
        grupo = [r for r in resumo if r["cenario"] == "aleatorio"]
        ns = [r["n"] for r in grupo]
        escala = grupo[-1][campo] / (ns[-1] * math.log2(ns[-1]))
        ax.plot(ns, [escala * n * math.log2(n) for n in ns], "--", color="gray",
                label="n log₂(n), ajustado ao último ponto aleatório")
        ax.set(xlabel="Quantidade de chamados", ylabel=unidade, title=titulo)
        ax.grid(alpha=0.25)
        ax.legend()
        fig.savefig(pasta / nome, dpi=150)
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tamanhos", nargs="+", type=int, default=[128, 512, 2048, 8192, 16384])
    parser.add_argument("--amostras", type=int, default=5)
    parser.add_argument("--repeticoes", type=int, default=3)
    parser.add_argument("--semente", type=int, default=36)
    parser.add_argument("--saida", type=Path, default=Path("resultados"))
    args = parser.parse_args()
    if min(args.tamanhos) < 2 or args.amostras < 1 or args.repeticoes < 1:
        parser.error("Tamanhos devem ser >= 2; amostras e repetições devem ser >= 1.")
    try:
        import matplotlib
    except ImportError:
        parser.error("Instale as dependências: python -m pip install -r requirements.txt")
    tamanhos = sorted(set(args.tamanhos))
    medicoes = executar(tamanhos, args.amostras, args.repeticoes, args.semente)
    resumo = resumir(medicoes)
    args.saida.mkdir(parents=True, exist_ok=True)
    escrever_csv(args.saida / "medicoes.csv", medicoes)
    escrever_csv(args.saida / "resumo.csv", resumo)
    metadados = dict(
        python=platform.python_version(), plataforma=platform.platform(),
        matplotlib=matplotlib.__version__, tamanhos=tamanhos,
        amostras=args.amostras, repeticoes=args.repeticoes, semente=args.semente,
        relogio="perf_counter_ns", trace=False,
    )
    (args.saida / "ambiente.json").write_text(
        json.dumps(metadados, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    gerar_graficos(resumo, args.saida)
    for linha in resumo:
        print(f"n={linha['n']:>6} {linha['cenario']:<9} "
              f"mediana={linha['tempo_mediano_ms']:.3f} ms "
              f"comparações={linha['comparacoes_medias']:.1f}")
    print(f"CSVs, gráficos e ambiente salvos em {args.saida}/")


if __name__ == "__main__":
    main()
