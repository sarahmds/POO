import streamlit as st
import auth

class AbrirContaUI:
    def main():
        st.header("Abrir Conta no Sistema")

        if "conta_criada" not in st.session_state:
            st.session_state.conta_criada = False

        tipo_usuario = st.selectbox("Tipo de usuário", ["Cliente", "Profissional"])

        nome = st.text_input("Informe o nome")
        email = st.text_input("Informe o e-mail")
        fone = st.text_input("Informe o fone") if tipo_usuario == "Cliente" else None
        profissao = st.text_input("Informe a profissão") if tipo_usuario == "Profissional" else None
        senha = st.text_input("Informe a senha", type="password")

        if st.button("Criar Conta"):
            if not nome or not email or not senha:
                st.error("Nome, e-mail e senha são obrigatórios")
                return

            if tipo_usuario == "Cliente":
                auth.cliente_inserir_raw(nome, email, fone, senha)
            else:  # Profissional
                auth.profissional_inserir_raw(nome, profissao, email, senha)

            st.session_state.conta_criada = True

        if st.session_state.conta_criada:
            st.success(f"Conta de {tipo_usuario} criada com sucesso!")
            st.session_state.conta_criada = False
