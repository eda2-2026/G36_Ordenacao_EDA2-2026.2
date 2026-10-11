import pytest

from atendimento import Chamado, FilaAtendimento
from merge_sort import Estatisticas


@pytest.mark.parametrize("campo,valor", [
    ("cliente", " "), ("descricao", ""), ("cliente", None),
    ("prioridade", 0), ("prioridade", 5), ("prioridade", True),
    ("prioridade", "1"), ("prioridade", 1.5),
    ("horario", "9:00"), ("horario", "24:00"), ("horario", "12:60"),
    ("horario", "09:00\n"), ("horario", None),
])
def test_validacoes(campo, valor):
    dados = dict(cliente="Ana", descricao="Sem acesso", prioridade=1, horario="09:00")
    dados[campo] = valor
    with pytest.raises(ValueError):
        Chamado(**dados)


def test_normaliza_textos_e_aceita_limites():
    assert Chamado(" Ana ", " Falha ", 1, "00:00").cliente == "Ana"
    assert Chamado("Ana", "Falha", 4, "23:59").horario == "23:59"


def test_fila_prioridade_horario_estabilidade_e_atendimento():
    fila = FilaAtendimento()
    baixo = fila.registrar("A", "Falha", 4, "07:00")
    primeiro = fila.registrar("B", "Falha", 1, "09:00")
    segundo = fila.registrar("C", "Falha", 1, "09:00")
    cedo = fila.registrar("D", "Falha", 1, "08:00")
    esperado = [cedo, primeiro, segundo, baixo]
    ordenados, estatisticas = fila.listar_ordenados()
    assert ordenados == esperado
    assert estatisticas.comparacoes > 0
    ordenados.clear()
    assert len(fila) == 4
    for chamado in esperado:
        assert fila.atender_proximo()[0] is chamado
    assert fila.atender_proximo() == (None, Estatisticas())


def test_registro_invalido_nao_altera_fila():
    fila = FilaAtendimento()
    with pytest.raises(ValueError):
        fila.registrar("Ana", "Falha", 7, "09:00")
    assert len(fila) == 0


def test_csv_preserva_textos_empates_e_remocoes(tmp_path):
    caminho = tmp_path / "chamados.csv"
    fila = FilaAtendimento()
    fila.registrar("João", 'Falha, com "aspas"\ne nova linha', 2, "10:00")
    fila.registrar("Lúcia", "Conexão", 2, "10:00")
    urgente = fila.registrar("Ana", "Servidor", 1, "11:00")
    fila.salvar_csv(caminho)
    restaurada = FilaAtendimento()
    restaurada.carregar_csv(caminho)
    assert restaurada.listar_ordenados()[0] == fila.listar_ordenados()[0]
    assert restaurada.atender_proximo()[0] == urgente
    restaurada.salvar_csv(caminho)
    restaurada.carregar_csv(caminho)
    assert [c.cliente for c in restaurada.listar_ordenados()[0]] == ["João", "Lúcia"]


@pytest.mark.parametrize("conteudo", [
    "", "nome,prioridade\nAna,1\n",
    "cliente,descricao,prioridade,horario\nAna,Falha,1,09:00\nB,Falha,5,10:00\n",
    "cliente,descricao,prioridade,horario\nAna,Falha,1\n",
    "cliente,descricao,prioridade,horario\nAna,Falha,1,09:00,extra\n",
    'cliente,descricao,prioridade,horario\nAna,"campo sem fechamento',
])
def test_csv_invalido_preserva_fila(tmp_path, conteudo):
    caminho = tmp_path / "invalido.csv"
    caminho.write_text(conteudo, encoding="utf-8")
    fila = FilaAtendimento()
    existente = fila.registrar("Existente", "Falha", 2, "08:00")
    with pytest.raises(ValueError):
        fila.carregar_csv(caminho)
    assert fila.listar_ordenados()[0] == [existente]


def test_csv_ausente_preserva_fila(tmp_path):
    fila = FilaAtendimento()
    existente = fila.registrar("Ana", "Falha", 1, "09:00")
    with pytest.raises(FileNotFoundError):
        fila.carregar_csv(tmp_path / "ausente.csv")
    assert fila.listar_ordenados()[0] == [existente]


def test_csv_de_fila_vazia_substitui_fila(tmp_path):
    caminho = tmp_path / "vazio.csv"
    FilaAtendimento().salvar_csv(caminho)
    fila = FilaAtendimento()
    fila.registrar("Ana", "Falha", 1, "09:00")
    fila.carregar_csv(caminho)
    assert fila.listar_ordenados() == ([], Estatisticas())
