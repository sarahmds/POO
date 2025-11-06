import streamlit as st
from views import View

class PerfiladminUI:

    @staticmethod
    def main():
        st.header("Meus Dados")

        try:
            if "usuario_id" not in st.session_state or st.session_state.get("usuario_tipo") != "admin":
                st.warning("Nenhum usuário admin logado")
                return

            usuario_id = st.session_state["usuario_id"]

            admin = View.cliente_listar_id(usuario_id)
            if not admin:
                st.warning("Dados do usuário não encontrados")
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
                    st.session_state["usuario_nome"] = nome
                    st.success("admin atualizado com sucesso!")
                except ValueError as ve:
                    st.error(f"Erro de validação: {ve}")
                except Exception as e:
                    st.error(f"Erro ao atualizar admin: {e}")

        except Exception as e:
            st.error(f"Erro ao carregar perfil do admin: {e}")
