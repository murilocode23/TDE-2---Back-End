"""Fixtures dos testes: app com SQLite em memória, criada a partir do schema.sql."""
import pytest

from app import create_app
from app.database_init import executar_schema

ADMIN = ("admin@exemplo.com", "123456")        # id 1, tipo admin
AUTOR1 = ("autor1@exemplo.com", "654321")      # id 2, tipo autor (criou as avaliações 1 e 2)
AUTOR2 = ("autor2@exemplo.com", "213246")      # id 3, tipo autor (sem avaliações)


@pytest.fixture()
def variaveis_ambiente(monkeypatch):
    monkeypatch.setenv("DB_DIALECT", "sqlite")
    monkeypatch.setenv("DB_NAME", ":memory:")
    monkeypatch.setenv("JWT_SECRET_KEY", "chave-so-para-testes-com-mais-de-32-bytes-ok")
    monkeypatch.setenv("JWT_EXPIRES_MINUTES", "5")


@pytest.fixture()
def app(variaveis_ambiente):
    app = create_app()
    with app.app_context():
        executar_schema()
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def cabecalhos(client):
    """Devolve uma função: cabecalhos(ADMIN) -> {"Authorization": "Bearer ..."}"""

    def _fazer_login(credenciais):
        email, senha = credenciais
        resposta = client.post("/auth/login", json={"email": email, "senha": senha})
        assert resposta.status_code == 200, resposta.get_json()
        return {"Authorization": f"Bearer {resposta.get_json()['access_token']}"}

    return _fazer_login
