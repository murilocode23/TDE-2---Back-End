"""Tabelas de associação N:N (usuário <-> curso e usuário <-> disciplina)."""
from app.extensions import db

usuario_curso = db.Table(
    "usuario_curso",
    db.Column("usuario_id", db.Integer, db.ForeignKey("usuario.id"), primary_key=True),
    db.Column("curso_id", db.Integer, db.ForeignKey("curso.id"), primary_key=True),
)

usuario_disciplina = db.Table(
    "usuario_disciplina",
    db.Column("usuario_id", db.Integer, db.ForeignKey("usuario.id"), primary_key=True),
    db.Column("disciplina_id", db.Integer, db.ForeignKey("disciplina.id"), primary_key=True),
)
