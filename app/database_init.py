"""Cria o banco a partir do schema.sql (o script SQL entregue ao professor)."""
from pathlib import Path

from sqlalchemy import inspect

from app.extensions import db

CAMINHO_SCHEMA = Path(__file__).resolve().parent.parent / "schema.sql"


def _comandos_sql(script):
    sem_comentarios = "\n".join(
        linha for linha in script.splitlines() if not linha.strip().startswith("--")
    )
    return [c.strip() for c in sem_comentarios.split(";") if c.strip()]


def banco_ja_inicializado():
    return inspect(db.engine).has_table("usuario")


def executar_schema(resetar=False):
    if resetar:
        db.drop_all()
    script = CAMINHO_SCHEMA.read_text(encoding="utf-8")
    with db.engine.begin() as conexao:
        for comando in _comandos_sql(script):
            conexao.exec_driver_sql(comando)
