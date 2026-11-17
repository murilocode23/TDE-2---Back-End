"""Endpoints de autenticação. O login é o ÚNICO endpoint público do sistema."""
from flask import Blueprint, jsonify

from app.controllers.auth_controller import AuthController
from app.errors import RequisicaoInvalida
from app.security.auth import usuario_logado
from app.utils.request import obter_json_obrigatorio

bp = Blueprint("auth", __name__, url_prefix="/auth")
controller = AuthController()


@bp.post("/login")
def login():
    """Body JSON: {"email": "...", "senha": "..."} -> 200 {"access_token": "...", ...}"""
    dados = obter_json_obrigatorio("email", "senha")
    if not isinstance(dados["email"], str) or not isinstance(dados["senha"], str):
        raise RequisicaoInvalida("Os campos 'email' e 'senha' devem ser texto.")
    resultado = controller.login(dados["email"].strip().lower(), dados["senha"])
    return jsonify(resultado), 200


@bp.get("/me")
def me():
    """Dados do usuário dono do token (útil para testar a autenticação)."""
    return jsonify(usuario_logado().to_dict()), 200
