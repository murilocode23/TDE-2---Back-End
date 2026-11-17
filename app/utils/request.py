"""Leitura e validação de dados da requisição."""
from flask import request

from app.errors import RequisicaoInvalida


def obter_json_obrigatorio(*campos):
    """Devolve o JSON do corpo, exigindo que os campos informados existam."""
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        raise RequisicaoInvalida("O corpo da requisição deve ser um JSON (Content-Type: application/json).")

    faltando = [
        campo for campo in campos
        if dados.get(campo) is None or (isinstance(dados[campo], str) and not dados[campo].strip())
    ]
    if faltando:
        raise RequisicaoInvalida(f"Campos obrigatórios ausentes: {', '.join(faltando)}")
    return dados


def _inteiro_positivo(nome, padrao):
    bruto = request.args.get(nome)
    if bruto is None:
        return padrao
    try:
        valor = int(bruto)
    except ValueError:
        raise RequisicaoInvalida(f"O parâmetro '{nome}' deve ser um número inteiro.")
    if valor < 1:
        raise RequisicaoInvalida(f"O parâmetro '{nome}' deve ser maior que zero.")
    return valor


def obter_paginacao():
    """Lê ?page=1&per_page=10 da URL."""
    return _inteiro_positivo("page", 1), _inteiro_positivo("per_page", 10)
