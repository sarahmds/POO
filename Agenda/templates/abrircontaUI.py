import streamlit as st
class AbrirContaUI:
    """Interface de usuário para a abertura de conta de cliente."""
    def main():
        st.header("Abrir Conta no Sistema")

        if "conta_criada" not in st.session_state:
            st.session_state.conta_criada = False

        nome = st.text_input("Informe o nome")
        email = st.text_input("Informe o e-mail")
        fone = st.text_input("Informe o telefone")
        senha = st.text_input("Informe a senha", type="password")

        if st.button("Criar Conta"):
            if not nome or not email or not senha:
                st.error("Nome, e-mail e senha são obrigatórios")
                return

            auth.cliente_inserir_raw(nome, email, fone, senha)
            st.session_state.conta_criada = True

        if st.session_state.conta_criada:
            st.success("Conta de cliente criada com sucesso!")
            st.session_state.conta_criada = False 
