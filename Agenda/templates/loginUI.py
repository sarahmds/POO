import streamlit as st
import auth

class LoginUI:
    def main():
        st.header("Entrar no Sistema")

        tipo_usuario = st.selectbox("Tipo de usuário", ["Cliente", "Profissional"])
        email = st.text_input("Informe o e-mail")
        senha = st.text_input("Informe a senha", type="password")

        if st.button("Entrar"):
            if tipo_usuario == "Cliente":
                c = auth.cliente_autenticar(email, senha)
                if c is not None:
                    st.session_state["usuario_id"] = c["id"]
                    st.session_state["usuario_nome"] = c["nome"]
                    st.session_state["usuario_tipo"] = "cliente"
                    st.success(f"Login realizado como cliente: {c['nome']}")
                    st.session_state["logado"] = True
                    return
            else:  # Profissional
                p = auth.profissional_autenticar(email, senha)
                if p is not None:
                    st.session_state["usuario_id"] = p["id"]
                    st.session_state["usuario_nome"] = p["nome"]
                    st.session_state["usuario_tipo"] = "profissional"
                    st.success(f"Login realizado como profissional: {p['nome']}")
                    st.session_state["logado"] = True
                    return

            st.error("E-mail ou senha inválidos")
