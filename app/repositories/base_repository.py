"""
Camada de PERSISTÊNCIA: só conversa com o banco. Nenhuma regra de negócio aqui.
Cada repository herda desta classe e define `model`.
"""
from sqlalchemy import select

from app.extensions import db
from app.utils.pagination import paginar


class BaseRepository:
    model = None

    def buscar_por_id(self, id_):
        return db.session.get(self.model, id_)

    def salvar(self, entidade):
        try:
            db.session.add(entidade)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        return entidade

    def remover(self, entidade):
        try:
            db.session.delete(entidade)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def listar_paginado(self, page, per_page, filtros=()):
        """Listagem paginada no banco. `filtros` = lista de condições SQLAlchemy."""
        consulta = select(self.model)
        for filtro in filtros:
            consulta = consulta.where(filtro)
        return paginar(consulta.order_by(self.model.id), page, per_page)
