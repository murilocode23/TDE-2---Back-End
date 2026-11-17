"""
Configuração da aplicação.

REGRA DO PROFESSOR: url, nome do banco, usuário e senha NÃO podem ficar fixos
no código. Tudo é lido de variáveis de ambiente (arquivo .env vai ser desenvolvido).
"""
import os

from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()


class ConfigError(RuntimeError):
    """Variável de ambiente obrigatória ausente."""


def _obrigatoria(nome):
    valor = os.getenv(nome)
    if valor is None or valor.strip() == "":
        raise ConfigError(
            f"Variável de ambiente '{nome}' não definida. "
            "Copie .env.example para .env e preencha."
        )
    return valor.strip()


def montar_uri_banco():
    dialeto = _obrigatoria("DB_DIALECT")
    nome = _obrigatoria("DB_NAME")

    if dialeto == "sqlite":
        return f"sqlite:///{nome}"

    porta = os.getenv("DB_PORT")
    return URL.create(
        drivername=dialeto,
        username=_obrigatoria("DB_USER"),
        password=_obrigatoria("DB_PASSWORD"),
        host=_obrigatoria("DB_HOST"),
        port=int(porta) if porta else None,
        database=nome,
    )


class Config:
    """Lida na criação da app (create_app), sempre a partir do ambiente."""

    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = montar_uri_banco()
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.JWT_SECRET_KEY = _obrigatoria("JWT_SECRET_KEY")
        self.JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))
        # Senha usada no reset feito por admin (opcional até alguém precisar dela)
        self.SENHA_PADRAO = os.getenv("SENHA_PADRAO") or None
