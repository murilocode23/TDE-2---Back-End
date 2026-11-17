"""Geração e validação do token JWT."""
from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app

from app.errors import NaoAutenticado


class JwtService:
    ALGORITMO = "HS256"

    @staticmethod
    def gerar_token(usuario):
        agora = datetime.now(timezone.utc)
        expira = agora + timedelta(minutes=current_app.config["JWT_EXPIRES_MINUTES"])
        payload = {
            "sub": str(usuario.id),
            "email": usuario.email,
            "tipo": usuario.tipo,
            "iat": agora,
            "exp": expira,
        }
        return jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm=JwtService.ALGORITMO)

    @staticmethod
    def validar_token(token):
        try:
            return jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=[JwtService.ALGORITMO],
            )
        except jwt.ExpiredSignatureError:
            raise NaoAutenticado("Token expirado")
        except jwt.InvalidTokenError:
            raise NaoAutenticado("Token inválido")
