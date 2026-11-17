from app.extensions import db
from app.models.associacoes import usuario_curso, usuario_disciplina


class Usuario(db.Model):
    __tablename__ = "usuario"

    TIPO_ADMIN = "admin"
    TIPO_AUTOR = "autor"
    TIPOS = (TIPO_ADMIN, TIPO_AUTOR)

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(255), nullable=False)  # sempre o HASH bcrypt

    cursos = db.relationship("Curso", secondary=usuario_curso, back_populates="usuarios")
    disciplinas = db.relationship("Disciplina", secondary=usuario_disciplina, back_populates="usuarios")

    def eh_admin(self):
        return self.tipo == self.TIPO_ADMIN

    def to_dict(self):
        """Nunca inclui a senha."""
        return {"id": self.id, "email": self.email, "nome": self.nome, "tipo": self.tipo}
