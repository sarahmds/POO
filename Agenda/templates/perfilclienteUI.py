import streamlit as st
import auth

class PerfilClienteUI:
    """Interface para o Cliente visualizar e atualizar seus próprios dados."""
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

        nome_atual = op.get("nome","")
        email_atual = op.get("email","")
        fone_atual = op.get("fone","")
        senha_atual = op.get("senha","")

        nome = st.text_input("Informe o novo nome", nome_atual)
        email = st.text_input("Informe o novo e-mail", email_atual)
        fone = st.text_input("Informe o novo fone", fone_atual)
        
        nova_senha = st.text_input("Informe a nova senha (deixe vazio para manter a atual)", type="password")
        
        senha_para_atualizar = nova_senha if nova_senha else senha_atual


        if st.button("Atualizar"):
            if not nome or not email:
                st.error("Nome e E-mail são obrigatórios")
                return
                
            auth.cliente_atualizar_raw(usuario_id, nome, email, fone, senha_para_atualizar)
            
            if nome != nome_atual:
                 st.session_state["usuario_nome"] = nome
                 
            st.success("Cliente atualizado com sucesso!")
            st.session_state["cliente_atualizado"] = True
