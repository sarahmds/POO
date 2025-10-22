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
            try:
                if not nome or not email or not senha:
                    raise ValueError("Nome, e-mail e senha são obrigatórios.")

                View.cliente_inserir(nome, email, fone, senha)
                st.success("Conta criada com sucesso! Você já pode logar.")

            except ValueError as ve:
                st.error(f"Erro de validação: {ve}")

            except Exception as e:
                st.error(f"Ocorreu um erro ao criar a conta: {e}")
