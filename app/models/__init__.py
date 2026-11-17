"""Importar tudo aqui garante que o SQLAlchemy conheça todas as tabelas."""
from app.models.associacoes import usuario_curso, usuario_disciplina  # noqa: F401
from app.models.avaliacao import Avaliacao, AvaliacaoQuestao  # noqa: F401
from app.models.curso import Curso  # noqa: F401
from app.models.disciplina import Disciplina  # noqa: F401
from app.models.questao import OpcaoQuestao, Questao  # noqa: F401
from app.models.template import Template  # noqa: F401
from app.models.usuario import Usuario  # noqa: F401
