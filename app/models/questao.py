from app.extensions import db


class Questao(db.Model):
    __tablename__ = "questao"

    TIPOS = ("aberta", "múltipla escolha")
    NIVEIS_DIFICULDADE = ("fácil", "média", "difícil")

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text)
    tipo = db.Column(db.String(100))
    nivel_dificuldade = db.Column(db.Text)
    disciplina_id = db.Column(db.Integer, db.ForeignKey("disciplina.id"), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    disciplina = db.relationship("Disciplina")
    autor = db.relationship("Usuario")
    opcoes = db.relationship(
        "OpcaoQuestao", back_populates="questao", cascade="all, delete-orphan", order_by="OpcaoQuestao.id"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "tipo": self.tipo,
            "nivel_dificuldade": self.nivel_dificuldade,
            "disciplina_id": self.disciplina_id,
            "autor_id": self.autor_id,
            "opcoes": [opcao.to_dict() for opcao in self.opcoes],
        }


class OpcaoQuestao(db.Model):
    __tablename__ = "opcao_questao"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text)
    correta = db.Column(db.Boolean)
    questao_id = db.Column(db.Integer, db.ForeignKey("questao.id"), nullable=False)

    questao = db.relationship("Questao", back_populates="opcoes")

    def to_dict(self):
        return {"id": self.id, "descricao": self.descricao, "correta": self.correta}
