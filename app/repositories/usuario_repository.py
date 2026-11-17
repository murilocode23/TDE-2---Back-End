from sqlalchemy import select

from app.extensions import db
from app.models.usuario import Usuario
from app.repositories.base_repository import BaseRepository


class UsuarioRepository(BaseRepository):
    model = Usuario

    def buscar_por_email(self, email):
        return db.session.scalar(select(Usuario).where(Usuario.email == email))
