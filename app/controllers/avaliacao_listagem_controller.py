"""
Regras de negócio das LISTAGENS de avaliações (parte do Murilo).
As permissões (admin x autor) são aplicadas na camada de serviços.
O CRUD de avaliações (Stephanie) fica em outro controller, para não dar conflito no git.
"""
from app.errors import NaoEncontrado
from app.repositories.avaliacao_repository import AvaliacaoRepository
from app.repositories.disciplina_repository import DisciplinaRepository
from app.utils.pagination import serializar_pagina


class AvaliacaoListagemController:
    def __init__(self):
        self.avaliacoes = AvaliacaoRepository()
        self.disciplinas = DisciplinaRepository()

    def _exigir_disciplina(self, disciplina_id):
        if self.disciplinas.buscar_por_id(disciplina_id) is None:
            raise NaoEncontrado("Disciplina não encontrada")

    def listar_todas(self, page, per_page):
        return serializar_pagina(self.avaliacoes.listar(page, per_page))

    def listar_por_disciplina(self, disciplina_id, page, per_page):
        self._exigir_disciplina(disciplina_id)
        return serializar_pagina(self.avaliacoes.listar(page, per_page, disciplina_id=disciplina_id))

    def listar_do_autor(self, autor_id, page, per_page):
        return serializar_pagina(self.avaliacoes.listar(page, per_page, autor_id=autor_id))

    def listar_do_autor_por_disciplina(self, autor_id, disciplina_id, page, per_page):
        self._exigir_disciplina(disciplina_id)
        return serializar_pagina(
            self.avaliacoes.listar(page, per_page, disciplina_id=disciplina_id, autor_id=autor_id)
        )
