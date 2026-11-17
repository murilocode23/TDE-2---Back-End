from app.models.questao import Questao
from app.repositories.base_repository import BaseRepository


class QuestaoRepository(BaseRepository):
    model = Questao
