"""Modelo de chamado, fila por prioridade e persistência explícita em CSV."""

import csv
import re
from dataclasses import dataclass
from pathlib import Path

from merge_sort import Estatisticas, merge_sort

CAMPOS_CSV = ("cliente", "descricao", "prioridade", "horario")


@dataclass(frozen=True)
class Chamado:
    cliente: str
    descricao: str
    prioridade: int
    horario: str

    def __post_init__(self) -> None:
        for campo in ("cliente", "descricao"):
            valor = getattr(self, campo)
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError(f"{campo} deve ser um texto não vazio.")
            object.__setattr__(self, campo, valor.strip())
        if type(self.prioridade) is not int or not 1 <= self.prioridade <= 4:
            raise ValueError("Prioridade deve ser um inteiro de 1 a 4.")
        if not isinstance(self.horario, str) or not re.fullmatch(
            r"(?:[01][0-9]|2[0-3]):[0-5][0-9]", self.horario
        ):
            raise ValueError("Horário deve estar no formato HH:MM, de 00:00 a 23:59.")


class FilaAtendimento:
    """Mantém a ordem de registro para preservar empates após salvar/carregar.

    Os horários se referem a um mesmo dia, conforme o formato do projeto.
    Registrar e atender alteram a memória; salvar_csv persiste essas mudanças.
    """

    def __init__(self) -> None:
        self._chamados: list[Chamado] = []

    def __len__(self) -> int:
        return len(self._chamados)

    def registrar(
        self, cliente: str, descricao: str, prioridade: int, horario: str
    ) -> Chamado:
        chamado = Chamado(cliente, descricao, prioridade, horario)
        self._chamados.append(chamado)
        return chamado

    def listar_ordenados(
        self, trace: list[tuple] | None = None
    ) -> tuple[list[Chamado], Estatisticas]:
        return merge_sort(
            self._chamados,
            chave=lambda chamado: (chamado.prioridade, chamado.horario),
            trace=trace,
        )

    def atender_proximo(self) -> tuple[Chamado | None, Estatisticas]:
        ordenados, estatisticas = self.listar_ordenados()
        if not ordenados:
            return None, estatisticas
        chamado = ordenados[0]
        self._chamados.remove(chamado)
        return chamado, estatisticas

    def salvar_csv(self, caminho: str | Path) -> None:
        with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(CAMPOS_CSV)
            for chamado in self._chamados:
                escritor.writerow(getattr(chamado, campo) for campo in CAMPOS_CSV)

    def carregar_csv(self, caminho: str | Path) -> None:
        """Substitui a fila somente se todo o arquivo for válido.

        Arquivos inexistentes geram FileNotFoundError; erros de formato geram
        ValueError. Nenhum desses erros remove os chamados já em memória.
        """
        chamados = []
        with open(caminho, encoding="utf-8", newline="") as arquivo:
            leitor = csv.DictReader(arquivo, strict=True)
            try:
                if leitor.fieldnames != list(CAMPOS_CSV):
                    raise ValueError(f"Cabeçalho CSV esperado: {','.join(CAMPOS_CSV)}")
                for linha in leitor:
                    try:
                        if None in linha or any(valor is None for valor in linha.values()):
                            raise ValueError("Quantidade de campos inválida.")
                        chamados.append(Chamado(
                            cliente=linha["cliente"],
                            descricao=linha["descricao"],
                            prioridade=int(linha["prioridade"]),
                            horario=linha["horario"],
                        ))
                    except ValueError as erro:
                        raise ValueError(f"CSV, linha {leitor.line_num}: {erro}") from erro
            except csv.Error as erro:
                raise ValueError(f"CSV inválido, linha {leitor.line_num}: {erro}") from erro
        self._chamados = chamados
