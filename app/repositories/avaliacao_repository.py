from app.models.avaliacao import Avaliacao
from app.repositories.base_repository import BaseRepository


class AvaliacaoRepository(BaseRepository):
    model = Avaliacao

    def listar(self, page, per_page, disciplina_id=None, autor_id=None):
        """Listagem paginada de avaliações, com filtros opcionais."""
        filtros = []
        if disciplina_id is not None:
            filtros.append(Avaliacao.disciplina_id == disciplina_id)
        if autor_id is not None:
            filtros.append(Avaliacao.autor_id == autor_id)
        return self.listar_paginado(page, per_page, filtros)
