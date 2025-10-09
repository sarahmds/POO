import streamlit as st
import auth

class PerfilProfissionalUI:
    """Interface para o Profissional visualizar e atualizar seus próprios dados."""
    def main():
        st.header("Meus Dados (Profissional)")

        if "usuario_id" not in st.session_state:
            st.write("Nenhum usuário logado")
            return

        usuario_id = st.session_state["usuario_id"]
        if st.session_state.get("usuario_tipo") != "profissional":
            st.write("Você não tem permissão para acessar esta página")
            return

        op = auth.profissional_listar_id_raw(usuario_id)
        if op is None:
            st.write("Dados do usuário não encontrados")
            return

        nome_atual = op.get("nome","")
        profissao_atual = op.get("profissao","")
        email_atual = op.get("email","")
        senha_atual = op.get("senha","") 

        nome = st.text_input("Informe o novo nome", nome_atual)
        profissao = st.text_input("Informe a nova profissão", profissao_atual)
        email = st.text_input("Informe o novo e-mail", email_atual)
        
        nova_senha = st.text_input("Informe a nova senha (deixe vazio para manter a atual)", type="password")

        senha_para_atualizar = nova_senha if nova_senha else senha_atual


        if st.button("Atualizar"):
            if not nome or not email or not profissao:
                st.error("Nome, E-mail e Profissão são obrigatórios")
                return

            auth.profissional_atualizar_raw(usuario_id, nome, profissao, email, senha_para_atualizar)
            
            if nome != nome_atual:
                 st.session_state["usuario_nome"] = nome
                 
            st.success("Profissional atualizado com sucesso!")
            st.session_state["profissional_atualizado"] = True
