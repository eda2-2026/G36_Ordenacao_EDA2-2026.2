import argparse

from atendimento import FilaAtendimento


def mostrar(chamado):
    return f"P{chamado.prioridade} {chamado.horario} {chamado.cliente}"


def mostrar_lista(chamados):
    return "[" + ", ".join(mostrar(chamado) for chamado in chamados) + "]"


def mostrar_passo(passo):
    recuo = "  " * passo[1]
    if passo[0] == "dividir":
        print(f"{recuo}dividir    {mostrar_lista(passo[2])}")
    else:
        print(
            f"{recuo}intercalar {mostrar_lista(passo[2])} + "
            f"{mostrar_lista(passo[3])} -> {mostrar_lista(passo[4])}"
        )


def mostrar_contagem(estatisticas):
    print(
        f"Comparações: {estatisticas.comparacoes} | "
        f"Movimentações: {estatisticas.movimentacoes}"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dados", default="chamados.csv")
    arquivo = parser.parse_args().dados

    fila = FilaAtendimento()
    try:
        fila.carregar_csv(arquivo)
    except FileNotFoundError:
        print("Arquivo não encontrado, começando com a fila vazia.")
    except ValueError as erro:
        print(f"Erro ao carregar {arquivo}: {erro}")
        return
    print(f"{len(fila)} chamado(s) na fila.")

    while True:
        print()
        print("1 - Registrar chamado")
        print("2 - Ver fila ordenada")
        print("3 - Atender próximo")
        print("4 - Merge Sort passo a passo")
        print("0 - Salvar e sair")
        opcao = input("Opção: ").strip()

        if opcao == "0":
            fila.salvar_csv(arquivo)
            print("Dados salvos.")
            break

        elif opcao == "1":
            cliente = input("Cliente: ")
            descricao = input("Descrição: ")
            prioridade = input("Prioridade (1 = crítica ... 4 = baixa): ").strip()
            horario = input("Horário (HH:MM): ").strip()
            if not prioridade.isdigit():
                print("Erro: a prioridade deve ser um número de 1 a 4.")
                continue
            try:
                chamado = fila.registrar(cliente, descricao, int(prioridade), horario)
                print("Registrado:", mostrar(chamado))
            except ValueError as erro:
                print("Erro:", erro)

        elif opcao == "2":
            ordenados, estatisticas = fila.listar_ordenados()
            if not ordenados:
                print("Fila vazia.")
            for posicao, chamado in enumerate(ordenados, start=1):
                print(f"{posicao}. {mostrar(chamado)} - {chamado.descricao}")
            mostrar_contagem(estatisticas)

        elif opcao == "3":
            chamado, estatisticas = fila.atender_proximo()
            if chamado is None:
                print("Fila vazia.")
            else:
                print("Atendido:", mostrar(chamado), "-", chamado.descricao)
                mostrar_contagem(estatisticas)

        elif opcao == "4":
            if len(fila) > 16:
                print("O passo a passo só funciona com até 16 chamados.")
                continue
            passos = []
            ordenados, estatisticas = fila.listar_ordenados(trace=passos)
            for passo in passos:
                mostrar_passo(passo)
            print("Resultado:", mostrar_lista(ordenados))
            mostrar_contagem(estatisticas)

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nEncerrado sem salvar.")
