import streamlit as st
import auth

class PerfilClienteUI:
    def main():
        st.header("Meus Dados")

        if "usuario_id" not in st.session_state:
            st.write("Nenhum usuário logado")
            return

        usuario_id = st.session_state["usuario_id"]
        op = auth.cliente_listar_id_raw(usuario_id)
        if op is None:
            st.write("Dados do usuário não encontrados")
            return

        nome = st.text_input("Informe o novo nome", op.get("nome",""))
        email = st.text_input("Informe o novo e-mail", op.get("email",""))
        fone = st.text_input("Informe o novo fone", op.get("fone",""))
        senha = st.text_input("Informe a nova senha", op.get("senha",""), type="password")

        if st.button("Atualizar"):
            auth.cliente_atualizar_raw(usuario_id, nome, email, fone, senha)
            st.success("Cliente atualizado com sucesso")

            st.session_state["cliente_atualizado"] = True
