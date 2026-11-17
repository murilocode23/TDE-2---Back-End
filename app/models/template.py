from app.extensions import db


class Template(db.Model):
    __tablename__ = "template"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    nome_arquivo = db.Column(db.String(255))

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "nome_arquivo": self.nome_arquivo}
