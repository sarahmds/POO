import streamlit as st
import json
from pathlib import Path
from views import View

BASE_DIR = Path(__file__).resolve().parent.parent
USUARIO_FILE = BASE_DIR / "usuario_logado.json"


def salvar_usuario(usuario: dict):
    """Salva o usuário logado em arquivo JSON."""
    USUARIO_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(USUARIO_FILE, "w", encoding="utf-8") as f:
        json.dump([usuario], f, ensure_ascii=False, indent=4)


def carregar_usuario() -> dict | None:
    """Carrega o usuário logado, se existir."""
    if not USUARIO_FILE.exists():
        return None
    try:
        with open(USUARIO_FILE, "r", encoding="utf-8") as f:
            usuarios = json.load(f)
            if isinstance(usuarios, list) and usuarios:
                return usuarios[0]
    except (json.JSONDecodeError, OSError):
        return None
    return None


def logout():
    """Remove o arquivo de sessão do usuário."""
    if USUARIO_FILE.exists():
        USUARIO_FILE.unlink()


class LoginUI:
    """Tela de login para clientes e profissionais."""

    @staticmethod
    def main():
        st.subheader("Entrar no Sistema")
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            try:
                if not email or not senha:
                    st.warning("Por favor, preencha e-mail e senha.")
                    return

                # Autentica cliente
                cliente = View.cliente_autenticar(email, senha)
                if cliente:
                    tipo = "admin" if email.lower() == "admin" else "cliente"
                    salvar_usuario({
                        "id": cliente["id"],
                        "nome": cliente["nome"],
                        "tipo": tipo
                    })
                    st.success(f"Bem-vindo, {cliente['nome']}!")
                    st.rerun()
                    return

                # Autentica profissional
                prof = View.profissional_autenticar(email, senha)
                if prof:
                    salvar_usuario({
                        "id": prof["id"],
                        "nome": prof["nome"],
                        "tipo": "profissional"
                    })
                    st.success(f"Bem-vindo, {prof['nome']}!")
                    st.rerun()
                    return

                st.error("Credenciais inválidas ou usuário não encontrado.")

            except Exception as e:
                st.error(f"Ocorreu um erro no login: {e}")
