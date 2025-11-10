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


class PerfilClienteUI:

    @staticmethod
    def main():
        st.header("Meus Dados")

        try:
            usuario = carregar_usuario_logado()

            if not usuario or usuario.get("tipo") != "cliente":
                st.warning("Nenhum usuário cliente logado.")
                return

            usuario_id = usuario["id"]

            cliente = View.cliente_listar_id(usuario_id)
            if not cliente:
                st.warning("Dados do usuário não encontrados.")
                return

            nome_atual = cliente.get_nome()
            email_atual = cliente.get_email()
            fone_atual = cliente.get_fone()
            senha_atual = cliente.get_senha()

            nome = st.text_input("Nome", nome_atual)
            email = st.text_input("E-mail", email_atual)
            fone = st.text_input("Telefone", fone_atual)
            nova_senha = st.text_input("Nova senha (deixe vazio para manter)", type="password")
            senha_para_atualizar = nova_senha if nova_senha else senha_atual

            if st.button("Atualizar"):
                try:
                    if not nome or not email:
                        raise ValueError("Nome e E-mail são obrigatórios.")

                    View.cliente_atualizar(usuario_id, nome, email, fone, senha_para_atualizar)

                    # Atualiza o nome do usuário logado no JSON
                    usuario["nome"] = nome
                    with open(USUARIO_FILE, "w", encoding="utf-8") as f:
                        json.dump([usuario], f, indent=4, ensure_ascii=False)

                    st.success("Dados atualizados com sucesso!")

                except ValueError as ve:
                    st.error(f"Erro de validação: {ve}")
                except Exception as e:
                    st.error(f"Erro ao atualizar cliente: {e}")

        except Exception as e:
            st.error(f"Erro ao carregar perfil do cliente: {e}")
