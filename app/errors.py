"""
Erros de negócio. Levante estes erros nos controllers; o handler converte
para JSON no formato {"erro": "mensagem"} com o status code correto.
"""
from flask import jsonify
from werkzeug.exceptions import HTTPException


class AppError(Exception):
    status_code = 500
    mensagem_padrao = "Erro interno do servidor"

    def __init__(self, mensagem=None):
        self.mensagem = mensagem or self.mensagem_padrao
        super().__init__(self.mensagem)


class RequisicaoInvalida(AppError):      # 400 - dados faltando/mal formatados
    status_code = 400
    mensagem_padrao = "Requisição inválida"


class NaoAutenticado(AppError):          # 401 - sem token / token inválido
    status_code = 401
    mensagem_padrao = "Autenticação necessária"


class AcessoNegado(AppError):            # 403 - logado, mas sem permissão
    status_code = 403
    mensagem_padrao = "Acesso negado"


class NaoEncontrado(AppError):           # 404
    status_code = 404
    mensagem_padrao = "Recurso não encontrado"


class Conflito(AppError):                # 409 - ex: e-mail já cadastrado
    status_code = 409
    mensagem_padrao = "Conflito com o estado atual do recurso"


class RegraDeNegocio(AppError):          # 422 - ex: quantidade de questões não bate
    status_code = 422
    mensagem_padrao = "Regra de negócio violada"


def registrar_handlers(app):
    @app.errorhandler(AppError)
    def _erro_de_negocio(erro):
        resposta = jsonify({"erro": erro.mensagem})
        if erro.status_code == 401:
            resposta.headers["WWW-Authenticate"] = "Bearer"
        return resposta, erro.status_code

    @app.errorhandler(HTTPException)
    def _erro_http(erro):
        return jsonify({"erro": erro.description}), erro.code

    @app.errorhandler(Exception)
    def _erro_inesperado(erro):
        app.logger.exception("Erro inesperado")
        return jsonify({"erro": "Erro interno do servidor"}), 500
