"""
Autenticação e autorização.

- autenticar_requisicao(): lê o header Authorization, valida o JWT e coloca o
  usuário em g.usuario_logado. É chamada automaticamente para TODO endpoint
  (ver create_app), exceto os de ENDPOINTS_PUBLICOS.
- usuario_logado(): devolve o usuário autenticado da requisição atual.
- roles_required("admin"): restringe o endpoint a certos tipos de usuário.
"""
from functools import wraps

from flask import g, request

from app.errors import AcessoNegado, NaoAutenticado
from app.repositories.usuario_repository import UsuarioRepository
from app.security.jwt_service import JwtService

# Único endpoint aberto ao público: o de login ("<blueprint>.<função>").
ENDPOINTS_PUBLICOS = {"auth.login"}


def _extrair_token():
    partes = request.headers.get("Authorization", "").split()
    if len(partes) != 2 or partes[0].lower() != "bearer":
        raise NaoAutenticado(
            "Token ausente ou mal formatado. Envie o header: Authorization: Bearer <token>"
        )
    return partes[1]


def autenticar_requisicao():
    if getattr(g, "usuario_logado", None) is not None:
        return g.usuario_logado

    payload = JwtService.validar_token(_extrair_token())
    try:
        usuario_id = int(payload["sub"])
    except (KeyError, ValueError):
        raise NaoAutenticado("Token inválido")

    usuario = UsuarioRepository().buscar_por_id(usuario_id)
    if usuario is None:
        raise NaoAutenticado("O usuário deste token não existe mais")

    g.usuario_logado = usuario
    return usuario


def usuario_logado():
    return g.usuario_logado


def roles_required(*tipos):
    """Uso: @roles_required("admin")  ou  @roles_required("admin", "autor")."""

    def decorador(funcao):
        @wraps(funcao)
        def envelope(*args, **kwargs):
            usuario = autenticar_requisicao()
            if usuario.tipo not in tipos:
                raise AcessoNegado(
                    f"Acesso negado: apenas usuários do tipo {' ou '.join(tipos)} podem acessar este recurso."
                )
            return funcao(*args, **kwargs)

        return envelope

    return decorador
