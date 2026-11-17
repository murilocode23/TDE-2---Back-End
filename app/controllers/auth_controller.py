"""Regras de negócio da autenticação."""
from flask import current_app

from app.errors import NaoAutenticado
from app.repositories.usuario_repository import UsuarioRepository
from app.security.jwt_service import JwtService
from app.security.passwords import verificar_senha


class AuthController:
    def __init__(self):
        self.usuarios = UsuarioRepository()

    def login(self, email, senha):
        usuario = self.usuarios.buscar_por_email(email)
        # Mesma mensagem para e-mail inexistente e senha errada (não revela qual falhou)
        if usuario is None or not verificar_senha(senha, usuario.senha):
            raise NaoAutenticado("E-mail ou senha incorretos")

        return {
            "access_token": JwtService.gerar_token(usuario),
            "token_type": "Bearer",
            "expira_em_minutos": current_app.config["JWT_EXPIRES_MINUTES"],
            "usuario": usuario.to_dict(),
        }
