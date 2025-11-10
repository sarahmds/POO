import streamlit as st
import json
from pathlib import Path
from views import View

BASE_DIR = Path(__file__).resolve().parent.parent
USUARIO_FILE = BASE_DIR / "usuario_logado.json"

def carregar_usuario_logado():
    if not USUARIO_FILE.exists():
        return None
    with open(USUARIO_FILE, "r", encoding="utf-8") as f:
        usuarios = json.load(f)
        return usuarios[0] if usuarios else None


class PerfilProfissionalUI:

    @staticmethod
    def main():
        st.header("Meus Dados")

        try:
            usuario = carregar_usuario_logado()

            if not usuario or usuario.get("tipo") != "profissional":
                st.warning("Nenhum usuário profissional logado.")
                return

            usuario_id = usuario["id"]

            prof = View.profissional_listar_id(usuario_id)
            if not prof:
                st.warning("Dados do usuário não encontrados.")
                return

            nome_atual = prof.get_nome()
            especialidade_atual = prof.get_especialidade()
            conselho_atual = prof.get_conselho()
            email_atual = prof.get_email()
            senha_atual = prof.get_senha()

            nome = st.text_input("Nome", nome_atual)
            especialidade = st.text_input("Especialidade", especialidade_atual)
            conselho = st.text_input("Conselho", conselho_atual)
            email = st.text_input("E-mail", email_atual)
            nova_senha = st.text_input("Nova senha (deixe vazio para manter)", type="password")
            senha_para_atualizar = nova_senha if nova_senha else senha_atual

            if st.button("Atualizar"):
                try:
                    if not nome or not email or not especialidade:
                        raise ValueError("Nome, E-mail e Especialidade são obrigatórios.")

                    View.profissional_atualizar(
                        usuario_id,
                        nome,
                        especialidade,
                        conselho,
                        email,
                        senha_para_atualizar
                    )

                    # Atualiza o nome do profissional no JSON de login
                    usuario["nome"] = nome
                    with open(USUARIO_FILE, "w", encoding="utf-8") as f:
                        json.dump([usuario], f, indent=4, ensure_ascii=False)

                    st.success("Dados atualizados com sucesso!")

                except ValueError as ve:
                    st.error(f"Erro de validação: {ve}")
                except Exception as e:
                    st.error(f"Erro ao atualizar profissional: {e}")

        except Exception as e:
            st.error(f"Erro ao carregar perfil do profissional: {e}")
