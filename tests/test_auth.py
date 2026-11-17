import pytest

from app import create_app
from app.config import ConfigError
from tests.conftest import ADMIN, AUTOR1


def test_login_com_sucesso_devolve_token_em_json(client):
    resposta = client.post("/auth/login", json={"email": "admin@exemplo.com", "senha": "123456"})
    corpo = resposta.get_json()
    assert resposta.status_code == 200
    assert resposta.mimetype == "application/json"
    assert corpo["token_type"] == "Bearer"
    assert corpo["access_token"]
    assert corpo["usuario"]["tipo"] == "admin"
    assert "senha" not in corpo["usuario"]


def test_login_normaliza_email(client):
    resposta = client.post("/auth/login", json={"email": "  ADMIN@Exemplo.com ", "senha": "123456"})
    assert resposta.status_code == 200


def test_login_senha_errada_retorna_401(client):
    resposta = client.post("/auth/login", json={"email": "admin@exemplo.com", "senha": "errada"})
    assert resposta.status_code == 401
    assert resposta.get_json() == {"erro": "E-mail ou senha incorretos"}


def test_login_email_inexistente_retorna_401_com_mesma_mensagem(client):
    resposta = client.post("/auth/login", json={"email": "ninguem@exemplo.com", "senha": "123456"})
    assert resposta.status_code == 401
    assert resposta.get_json()["erro"] == "E-mail ou senha incorretos"


def test_login_sem_campos_retorna_400(client):
    resposta = client.post("/auth/login", json={"email": "admin@exemplo.com"})
    assert resposta.status_code == 400
    assert "senha" in resposta.get_json()["erro"]


def test_login_exige_json_e_nao_formulario(client):
    resposta = client.post("/auth/login", data={"email": "admin@exemplo.com", "senha": "123456"})
    assert resposta.status_code == 400


def test_login_com_tipos_errados_retorna_400(client):
    resposta = client.post("/auth/login", json={"email": 123, "senha": ["x"]})
    assert resposta.status_code == 400


def test_endpoint_protegido_sem_token_retorna_401(client):
    resposta = client.get("/auth/me")
    assert resposta.status_code == 401
    assert "erro" in resposta.get_json()


def test_token_invalido_retorna_401(client):
    resposta = client.get("/auth/me", headers={"Authorization": "Bearer abc.def.ghi"})
    assert resposta.status_code == 401
    assert resposta.get_json()["erro"] == "Token inválido"


def test_header_mal_formatado_retorna_401(client):
    resposta = client.get("/auth/me", headers={"Authorization": "Token qualquercoisa"})
    assert resposta.status_code == 401


def test_me_com_token_valido(client, cabecalhos):
    resposta = client.get("/auth/me", headers=cabecalhos(AUTOR1))
    assert resposta.status_code == 200
    assert resposta.get_json()["email"] == "autor1@exemplo.com"


def test_token_expirado_retorna_401(app, client, monkeypatch):
    monkeypatch.setitem(app.config, "JWT_EXPIRES_MINUTES", -1)
    token = client.post("/auth/login", json={"email": ADMIN[0], "senha": ADMIN[1]}).get_json()["access_token"]
    resposta = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resposta.status_code == 401
    assert resposta.get_json()["erro"] == "Token expirado"


def test_novo_endpoint_sem_decorator_ja_nasce_protegido(variaveis_ambiente):
    """Regra do professor: TODO endpoint exige login, mesmo que o dev esqueça o decorator."""
    app = create_app()
    app.add_url_rule("/rota-esquecida", "rota_esquecida", lambda: "dados sigilosos")
    resposta = app.test_client().get("/rota-esquecida")
    assert resposta.status_code == 401


def test_rota_inexistente_retorna_404_em_json(client):
    resposta = client.get("/nao-existe")
    assert resposta.status_code == 404
    assert "erro" in resposta.get_json()


def test_variavel_de_ambiente_obrigatoria_ausente(variaveis_ambiente, monkeypatch):
    monkeypatch.delenv("JWT_SECRET_KEY")
    monkeypatch.setattr("app.config.load_dotenv", lambda *a, **k: None)
    with pytest.raises(ConfigError, match="JWT_SECRET_KEY"):
        create_app()
