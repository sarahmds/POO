# templates/loginUI.py
import streamlit as st
import json
from pathlib import Path
from views import View

BASE_DIR = Path(__file__).resolve().parent.parent
USUARIO_FILE = BASE_DIR / "usuario_logado.json"
def salvar_usuario(usuario: dict):
    USUARIO_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(USUARIO_FILE, "w", encoding="utf-8") as f:
        json.dump([usuario], f, ensure_ascii=False, indent=4)


def carregar_usuario() -> dict | None:
    if not USUARIO_FILE.exists():
        return None
    with open(USUARIO_FILE, "r", encoding="utf-8") as f:
        usuarios = json.load(f)
        if usuarios:
            return usuarios[0]
    return None


def logout():
    if USUARIO_FILE.exists():
        USUARIO_FILE.unlink()


class LoginUI:

    @staticmethod
    def main():
        st.subheader("Entrar no Sistema")
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            # Cliente
            cliente = View.cliente_autenticar(email, senha)
            if cliente:
                usuario = {
                    "id": cliente["id"],
                    "nome": cliente["nome"],
                    "tipo": "admin" if email.lower() == "admin" else "cliente"
                }
                salvar_usuario(usuario)
                st.rerun()
                return

            # Profissional
            prof = View.profissional_autenticar(email, senha)
            if prof:
                usuario = {
                    "id": prof["id"],
                    "nome": prof["nome"],
                    "tipo": "profissional"
                }
                salvar_usuario(usuario)
                st.rerun()
                return

            st.error("Credenciais inválidas ou usuário não encontrado.")
