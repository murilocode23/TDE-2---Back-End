from app.extensions import db
from app.models.associacoes import usuario_disciplina


class Disciplina(db.Model):
    __tablename__ = "disciplina"

    TURNOS = ("Vespertino", "Noturno")

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    carga_horaria = db.Column(db.Integer, nullable=False)
    turno = db.Column(db.String(50))
    curso_id = db.Column(db.Integer, db.ForeignKey("curso.id"), nullable=False)

    curso = db.relationship("Curso", back_populates="disciplinas")
    usuarios = db.relationship("Usuario", secondary=usuario_disciplina, back_populates="disciplinas")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "carga_horaria": self.carga_horaria,
            "turno": self.turno,
            "curso_id": self.curso_id,
        }
