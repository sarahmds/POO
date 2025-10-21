import streamlit as st
from views import View

class AbrirContaUI:
    """Tela para criar conta de cliente."""

    @staticmethod
    def main():
        st.header("Abrir Conta no Sistema")

        nome = st.text_input("Nome")
        email = st.text_input("E-mail")
        fone = st.text_input("Telefone")
        senha = st.text_input("Senha", type="password")

        if st.button("Criar Conta"):
            if not nome or not email or not senha:
                st.error("Nome, e-mail e senha são obrigatórios")
                return

            # Cria cliente no DAO
            View.cliente_inserir(nome, email, fone, senha)
            st.success("Conta criada com sucesso! Você já pode logar.")
