"""
Endpoints de LISTAGEM de avaliações (todos paginados: ?page=1&per_page=10).

  GET /avaliacoes                                     -> admin: todas
  GET /disciplinas/<id>/avaliacoes                    -> admin: todas da disciplina
  GET /avaliacoes/minhas                              -> usuário logado: as que ele criou
  GET /disciplinas/<id>/avaliacoes/minhas             -> usuário logado: as que ele criou na disciplina
"""
from flask import Blueprint, jsonify

from app.controllers.avaliacao_listagem_controller import AvaliacaoListagemController
from app.models.usuario import Usuario
from app.security.auth import roles_required, usuario_logado
from app.utils.request import obter_paginacao

bp = Blueprint("avaliacoes_listagem", __name__)
controller = AvaliacaoListagemController()


@bp.get("/avaliacoes")
@roles_required(Usuario.TIPO_ADMIN)
def listar_todas():
    page, per_page = obter_paginacao()
    return jsonify(controller.listar_todas(page, per_page)), 200


@bp.get("/disciplinas/<int:disciplina_id>/avaliacoes")
@roles_required(Usuario.TIPO_ADMIN)
def listar_por_disciplina(disciplina_id):
    page, per_page = obter_paginacao()
    return jsonify(controller.listar_por_disciplina(disciplina_id, page, per_page)), 200


@bp.get("/avaliacoes/minhas")
def listar_minhas():
    page, per_page = obter_paginacao()
    return jsonify(controller.listar_do_autor(usuario_logado().id, page, per_page)), 200


@bp.get("/disciplinas/<int:disciplina_id>/avaliacoes/minhas")
def listar_minhas_por_disciplina(disciplina_id):
    page, per_page = obter_paginacao()
    resultado = controller.listar_do_autor_por_disciplina(usuario_logado().id, disciplina_id, page, per_page)
    return jsonify(resultado), 200
