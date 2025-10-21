import streamlit as st
from views import View

class PerfilProfissionalUI:

    @staticmethod
    def main():
        st.header("Meus Dados")

        if "usuario_id" not in st.session_state or st.session_state.get("usuario_tipo") != "profissional":
            st.write("Nenhum usuário profissional logado")
            return

        usuario_id = st.session_state["usuario_id"]

        # Recupera objeto Profissional
        prof = View.profissional_listar_id(usuario_id)
        if not prof:
            st.write("Dados do usuário não encontrados")
            return

        # Atributos via getters
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
            if not nome or not email or not especialidade:
                st.error("Nome, E-mail e Especialidade são obrigatórios")
                return

            # Atualiza via DAO
            View.profissional_atualizar(usuario_id, nome, especialidade, conselho, email, senha_para_atualizar)
            st.session_state["usuario_nome"] = nome
            st.success("Profissional atualizado com sucesso!")
