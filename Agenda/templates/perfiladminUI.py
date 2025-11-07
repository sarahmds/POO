import streamlit as st
import json
from pathlib import Path
from views import View

DATA_DIR = Path("data")
USUARIOS_FILE = DATA_DIR / "usuario_logado.json"

def carregar_usuario_logado():
    if not USUARIOS_FILE.exists():
        return None
    with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
        usuarios = json.load(f)
        return usuarios[0] if usuarios else None


class PerfiladminUI:

    @staticmethod
    def main():
        st.header("Meus Dados")

        try:
            DATA_DIR.mkdir(exist_ok=True)
            usuario = carregar_usuario_logado()

            if not usuario or usuario.get("tipo") != "admin":
                st.warning("Nenhum usuário admin logado.")
                return

            usuario_id = usuario["id"]

            admin = View.cliente_listar_id(usuario_id)
            if not admin:
                st.warning("Dados do usuário não encontrados.")
                return

            nome_atual = admin.get_nome()
            email_atual = admin.get_email()
            fone_atual = admin.get_fone()
            senha_atual = admin.get_senha()

            nome = st.text_input("Nome", nome_atual)
            fone = st.text_input("Telefone", fone_atual)
            nova_senha = st.text_input("Nova senha (deixe vazio para manter)", type="password")
            senha_para_atualizar = nova_senha if nova_senha else senha_atual

            if st.button("Atualizar"):
                try:
                    if not nome or not email_atual:
                        raise ValueError("Nome e E-mail são obrigatórios.")

                    View.cliente_atualizar(usuario_id, nome, email_atual, fone, senha_para_atualizar)

                    # Atualiza o JSON de login com o novo nome
                    usuario["nome"] = nome
                    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
                        json.dump([usuario], f, indent=4, ensure_ascii=False)

                    st.success("Admin atualizado com sucesso!")
                except ValueError as ve:
                    st.error(f"Erro de validação: {ve}")
                except Exception as e:
                    st.error(f"Erro ao atualizar admin: {e}")

        except Exception as e:
            st.error(f"Erro ao carregar perfil do admin: {e}")
