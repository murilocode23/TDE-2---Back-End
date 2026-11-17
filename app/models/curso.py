from app.extensions import db
from app.models.associacoes import usuario_curso


class Curso(db.Model):
    __tablename__ = "curso"

    FORMATOS_AULA = ("presencial", "EAD", "semi-presencial")

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(400), nullable=False)
    formato_aula = db.Column(db.String(30), nullable=False)

    disciplinas = db.relationship("Disciplina", back_populates="curso")
    usuarios = db.relationship("Usuario", secondary=usuario_curso, back_populates="cursos")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "formato_aula": self.formato_aula,
        }
