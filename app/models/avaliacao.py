from app.extensions import db


class Avaliacao(db.Model):
    __tablename__ = "avaliacao"

    TIPOS = (
        "AV1", "AV1-SEGUNDA-CHAMADA", "AV1-ADAPTADA", "AV1-ADAPTADA-SEGUNDA-CHAMADA",
        "AV2", "AV2-SEGUNDA-CHAMADA", "AV2-ADAPTADA", "AV2-ADAPTADA-SEGUNDA-CHAMADA",
        "FINAL", "FINAL-SEGUNDA-CHAMADA", "FINAL-ADAPTADA", "FINAL-ADAPTADA-SEGUNDA-CHAMADA",
    )

    id = db.Column(db.Integer, primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey("curso.id"), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey("disciplina.id"), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    semestre = db.Column(db.Text)
    docente = db.Column(db.String(100), nullable=False)
    data_avaliacao = db.Column(db.Date)
    data_elaboracao = db.Column(db.Date)
    tipo = db.Column(db.Text)
    valor_avaliacao = db.Column(db.Integer, nullable=False)
    quantidade_questoes_multipla_escolha = db.Column(db.Integer, nullable=False)
    quantidade_questoes_abertas = db.Column(db.Integer, nullable=False)

    curso = db.relationship("Curso")
    disciplina = db.relationship("Disciplina")
    autor = db.relationship("Usuario")
    questoes = db.relationship("AvaliacaoQuestao", back_populates="avaliacao", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "curso_id": self.curso_id,
            "disciplina_id": self.disciplina_id,
            "autor_id": self.autor_id,
            "semestre": self.semestre,
            "docente": self.docente,
            "data_avaliacao": self.data_avaliacao.isoformat() if self.data_avaliacao else None,
            "data_elaboracao": self.data_elaboracao.isoformat() if self.data_elaboracao else None,
            "tipo": self.tipo,
            "valor_avaliacao": self.valor_avaliacao,
            "quantidade_questoes_multipla_escolha": self.quantidade_questoes_multipla_escolha,
            "quantidade_questoes_abertas": self.quantidade_questoes_abertas,
        }


class AvaliacaoQuestao(db.Model):
    __tablename__ = "avaliacao_questao"

    id = db.Column(db.Integer, primary_key=True)
    avaliacao_id = db.Column(db.Integer, db.ForeignKey("avaliacao.id"), nullable=False)
    questao_id = db.Column(db.Integer, db.ForeignKey("questao.id"), nullable=False)
    valor_questao = db.Column(db.Integer, nullable=False)

    avaliacao = db.relationship("Avaliacao", back_populates="questoes")
    questao = db.relationship("Questao")

    def to_dict(self):
        return {
            "id": self.id,
            "avaliacao_id": self.avaliacao_id,
            "questao_id": self.questao_id,
            "valor_questao": self.valor_questao,
        }
