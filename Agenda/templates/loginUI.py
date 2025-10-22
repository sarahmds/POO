import streamlit as st
from views import View

class LoginUI:

    @staticmethod
    def main():
        st.subheader("Entrar no Sistema")

        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            if email == "admin" and senha == "1234":
                st.session_state["usuario_id"] = 0
                st.session_state["usuario_nome"] = "Administrador"
                st.session_state["usuario_tipo"] = "admin"
                st.success("Login de Administrador realizado!")
                st.rerun()
                return

            cliente = View.cliente_autenticar(email, senha)
            if cliente:
                st.session_state["usuario_id"] = cliente["id"]
                st.session_state["usuario_nome"] = cliente["nome"]
                st.session_state["usuario_tipo"] = "cliente"
                st.success(f"Login de Cliente realizado! Bem-vindo(a), {cliente['nome']}")
                st.rerun()
                return

            prof = View.profissional_autenticar(email, senha)
            if prof:
                st.session_state["usuario_id"] = prof["id"]
                st.session_state["usuario_nome"] = prof["nome"]
                st.session_state["usuario_tipo"] = "profissional"
                st.success(f"Login de Profissional realizado! Bem-vindo(a), {prof['nome']}")
                st.rerun()
                return

            st.error("Credenciais inválidas ou usuário não encontrado.")
