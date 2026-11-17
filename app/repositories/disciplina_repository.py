from app.models.disciplina import Disciplina
from app.repositories.base_repository import BaseRepository


class DisciplinaRepository(BaseRepository):
    model = Disciplina
