import streamlit as st
from views import View

class LoginUI:
    """Interface de usuário para a tela de Login."""
    
    @staticmethod
    def main():
        st.subheader("Entrar no Sistema")
        
        email = st.text_input("Email", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_senha")
        
        if st.button("Entrar", key="login_button"):
            usuario_cliente = View.cliente_autenticar(email, senha)

            if usuario_cliente is None:
                usuario_profissional = View.profissional_autenticar(email, senha)
                
                if usuario_profissional:
                    st.session_state["usuario_id"] = usuario_profissional["id"]
                    st.session_state["usuario_nome"] = usuario_profissional["nome"]
                    st.session_state["usuario_tipo"] = "profissional"
                    st.success(f"Login de Profissional realizado! Bem-vindo(a), {usuario_profissional['nome']}.")
                    st.rerun()
                else:
                    st.error("Credenciais inválidas ou usuário não encontrado.")
            else:
                st.session_state["usuario_id"] = usuario_cliente["id"]
                st.session_state["usuario_nome"] = usuario_cliente["nome"]
                
                if email == "admin":
                    st.session_state["usuario_tipo"] = "admin"
                    st.success(f"Login de Administrador realizado! Bem-vindo(a), {usuario_cliente['nome']}.")
                else:
                    st.session_state["usuario_tipo"] = "cliente"
                    st.success(f"Login de Cliente realizado! Bem-vindo(a), {usuario_cliente['nome']}.")

                st.rerun()
