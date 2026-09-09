from getpass import getpass

from app.core.security import hash_senha
from app.db.session import SessionLocal
from app.models.enums import Perfil
from app.models.usuario import Usuario


def criar_usuario(db, nome: str, email: str, perfil: Perfil) -> Usuario:
    senha = getpass(f"Senha para {nome} ({email}): ")
    usuario = Usuario(nome=nome, email=email, senha_hash=hash_senha(senha), perfil=perfil)
    db.add(usuario)
    return usuario


def seed():
    db = SessionLocal()
    try:
        criar_usuario(db, "Ramon", "ramon@novaconquista.com.br", Perfil.ADMIN)
        criar_usuario(db, "Marivaldo", "marivaldo@novaconquista.com.br", Perfil.USER)
        db.commit()
        print("Usuarios criados com sucesso.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()