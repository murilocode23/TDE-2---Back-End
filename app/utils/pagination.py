"""
Paginação feita NO BANCO (LIMIT/OFFSET), como exige o professor
("paginação em disco"): nunca carregue a lista inteira e fatie em Python.

Toda listagem do sistema deve devolver este formato:
    {"items": [...], "page": 1, "per_page": 10, "total": 25, "pages": 3}
"""
from app.extensions import db

MAXIMO_POR_PAGINA = 100


def paginar(consulta, page, per_page):
    """`consulta` é um select() do SQLAlchemy, já com order_by."""
    pagina = db.paginate(
        consulta,
        page=page,
        per_page=per_page,
        max_per_page=MAXIMO_POR_PAGINA,
        error_out=False,
        count=True,
    )
    return {
        "items": pagina.items,
        "page": pagina.page,
        "per_page": pagina.per_page,
        "total": pagina.total,
        "pages": pagina.pages,
    }


def serializar_pagina(pagina, serializador=lambda entidade: entidade.to_dict()):
    return {**pagina, "items": [serializador(item) for item in pagina["items"]]}
