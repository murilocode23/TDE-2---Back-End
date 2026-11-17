from tests.conftest import ADMIN, AUTOR1, AUTOR2


def test_admin_lista_todas_as_avaliacoes_paginado(client, cabecalhos):
    resposta = client.get("/avaliacoes", headers=cabecalhos(ADMIN))
    corpo = resposta.get_json()
    assert resposta.status_code == 200
    assert set(corpo) == {"items", "page", "per_page", "total", "pages"}
    assert corpo["total"] == 2
    assert len(corpo["items"]) == 2
    assert corpo["items"][0]["data_avaliacao"] == "2026-10-15"


def test_paginacao_e_feita_com_page_e_per_page(client, cabecalhos):
    pagina1 = client.get("/avaliacoes?page=1&per_page=1", headers=cabecalhos(ADMIN)).get_json()
    pagina2 = client.get("/avaliacoes?page=2&per_page=1", headers=cabecalhos(ADMIN)).get_json()
    pagina3 = client.get("/avaliacoes?page=3&per_page=1", headers=cabecalhos(ADMIN)).get_json()
    assert (pagina1["total"], pagina1["pages"]) == (2, 2)
    assert [a["id"] for a in pagina1["items"]] == [1]
    assert [a["id"] for a in pagina2["items"]] == [2]
    assert pagina3["items"] == []


def test_parametros_de_paginacao_invalidos_retornam_400(client, cabecalhos):
    assert client.get("/avaliacoes?page=0", headers=cabecalhos(ADMIN)).status_code == 400
    assert client.get("/avaliacoes?per_page=abc", headers=cabecalhos(ADMIN)).status_code == 400


def test_autor_nao_pode_listar_todas(client, cabecalhos):
    resposta = client.get("/avaliacoes", headers=cabecalhos(AUTOR1))
    assert resposta.status_code == 403
    assert "erro" in resposta.get_json()


def test_listagem_exige_autenticacao(client):
    assert client.get("/avaliacoes").status_code == 401
    assert client.get("/avaliacoes/minhas").status_code == 401


def test_admin_lista_por_disciplina(client, cabecalhos):
    corpo = client.get("/disciplinas/2/avaliacoes", headers=cabecalhos(ADMIN)).get_json()
    assert corpo["total"] == 1
    assert corpo["items"][0]["disciplina_id"] == 2


def test_disciplina_sem_avaliacoes_retorna_lista_vazia(client, cabecalhos):
    resposta = client.get("/disciplinas/3/avaliacoes", headers=cabecalhos(ADMIN))
    assert resposta.status_code == 200
    assert resposta.get_json()["items"] == []


def test_disciplina_inexistente_retorna_404(client, cabecalhos):
    resposta = client.get("/disciplinas/999/avaliacoes", headers=cabecalhos(ADMIN))
    assert resposta.status_code == 404


def test_autor_nao_pode_listar_por_disciplina_como_admin(client, cabecalhos):
    assert client.get("/disciplinas/2/avaliacoes", headers=cabecalhos(AUTOR1)).status_code == 403


def test_autor_lista_somente_as_suas_avaliacoes(client, cabecalhos):
    autor1 = client.get("/avaliacoes/minhas", headers=cabecalhos(AUTOR1)).get_json()
    autor2 = client.get("/avaliacoes/minhas", headers=cabecalhos(AUTOR2)).get_json()
    assert autor1["total"] == 2
    assert all(a["autor_id"] == 2 for a in autor1["items"])
    assert autor2["total"] == 0


def test_autor_lista_suas_avaliacoes_por_disciplina(client, cabecalhos):
    corpo = client.get("/disciplinas/1/avaliacoes/minhas", headers=cabecalhos(AUTOR1)).get_json()
    assert corpo["total"] == 1
    assert corpo["items"][0]["disciplina_id"] == 1
    vazio = client.get("/disciplinas/1/avaliacoes/minhas", headers=cabecalhos(AUTOR2)).get_json()
    assert vazio["total"] == 0


def test_minhas_por_disciplina_inexistente_retorna_404(client, cabecalhos):
    resposta = client.get("/disciplinas/999/avaliacoes/minhas", headers=cabecalhos(AUTOR1))
    assert resposta.status_code == 404
