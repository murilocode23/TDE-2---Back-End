"""Fábrica da aplicação Flask (padrão Application Factory)."""
import click
from flask import Flask, request
from sqlalchemy import event
from sqlalchemy.engine import Engine

from app.config import Config
from app.errors import registrar_handlers
from app.extensions import db
from app.security.auth import ENDPOINTS_PUBLICOS, autenticar_requisicao


@event.listens_for(Engine, "connect")
def _ativar_foreign_keys_no_sqlite(conexao_dbapi, _registro):
    """SQLite ignora FOREIGN KEY por padrão; ligamos para a integridade valer."""
    if conexao_dbapi.__class__.__module__.startswith("sqlite3"):
        cursor = conexao_dbapi.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def _exigir_autenticacao_em_todos_os_endpoints(app):
    """
    REGRA DO PROFESSOR: todo endpoint exige autenticação, exceto o login.
    Aqui o padrão é NEGAR: ninguém precisa lembrar de colocar decorator
    para exigir login. Só endpoints listados em ENDPOINTS_PUBLICOS passam.
    """

    @app.before_request
    def _exigir_autenticacao():
        if request.endpoint is None or request.endpoint in ENDPOINTS_PUBLICOS:
            return None
        autenticar_requisicao()


def _registrar_comandos_cli(app):
    @app.cli.command("init-db")
    @click.option("--reset", is_flag=True, help="Apaga as tabelas existentes antes de recriar.")
    def init_db(reset):
        """Cria as tabelas e os dados de exemplo a partir do schema.sql."""
        from app.database_init import banco_ja_inicializado, executar_schema

        if banco_ja_inicializado() and not reset:
            click.echo("Banco já inicializado. Use --reset para apagar e recriar.")
            return
        executar_schema(resetar=reset)
        click.echo("Banco criado com sucesso a partir do schema.sql.")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    app.json.ensure_ascii = False   # acentos legíveis no JSON
    app.json.sort_keys = False

    db.init_app(app)
    from app import models  # noqa: F401  (carrega todos os models)

    registrar_handlers(app)
    _exigir_autenticacao_em_todos_os_endpoints(app)

    from app.services import registrar_services
    registrar_services(app)

    _registrar_comandos_cli(app)
    return app
