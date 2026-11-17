"""Hash de senha com bcrypt. NUNCA salve senha em texto puro."""
import bcrypt

LIMITE_BYTES_BCRYPT = 72


def hash_senha(senha):
    dados = senha.encode("utf-8")
    if len(dados) > LIMITE_BYTES_BCRYPT:
        raise ValueError("A senha deve ter no máximo 72 bytes.")
    return bcrypt.hashpw(dados, bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha, senha_hash):
    try:
        return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))
    except ValueError:
        return False
