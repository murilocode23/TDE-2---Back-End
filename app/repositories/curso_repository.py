from app.models.curso import Curso
from app.repositories.base_repository import BaseRepository


class CursoRepository(BaseRepository):
    model = Curso
