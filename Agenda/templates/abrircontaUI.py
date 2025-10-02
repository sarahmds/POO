import streamlit as st
import auth

class AbrirContaUI:
    def main():
        st.header("Abrir Conta no Sistema")

        if "conta_criada" not in st.session_state:
            st.session_state.conta_criada = False

        nome = st.text_input("Informe o nome")
        email = st.text_input("Informe o e-mail")
        fone = st.text_input("Informe o fone")
        senha = st.text_input("Informe a senha", type="password")

        if st.button("Inserir"):
            if not nome or not email:
                st.error("Nome e e-mail são obrigatórios")
                return
            auth.cliente_inserir_raw(nome, email, fone, senha)
            st.session_state.conta_criada = True


        if st.session_state.conta_criada:
            st.success("Conta criada com sucesso!")
            st.session_state.conta_criada = False  
