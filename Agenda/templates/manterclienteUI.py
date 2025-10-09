import streamlit as st
from views import View
from models.cliente import Cliente

class ManterClienteUI:
    
    @staticmethod
    def cadastrar():
        st.subheader("Cadastrar Novo Cliente")
        
        with st.form("form_cliente_cadastro"):
            nome = st.text_input("Nome")
            email = st.text_input("Email (Login)")
            fone = st.text_input("Telefone")
            senha = st.text_input("Senha", type="password") 
            
            submitted = st.form_submit_button("Cadastrar Cliente")

            if submitted:
                try:
                    View.cliente_inserir(nome, email, fone, senha) 
                    st.success(f"Cliente '{nome}' cadastrado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao cadastrar: {e}")

    @staticmethod
    def atualizar():
        st.subheader("Atualizar Cliente")
        clientes = View.cliente_listar()
        
        opcoes = {f"{c.get_nome()} ({c.get_email()}) - ID: {c.get_id()}": c for c in clientes}
        selecionado_str = st.selectbox("Selecione o cliente para atualizar", list(opcoes.keys()))
        
        if selecionado_str:
            op: Cliente = opcoes[selecionado_str]
            
            with st.form("form_cliente_atualizar"):
                nome = st.text_input("Novo Nome", op.get_nome())
                email = st.text_input("Novo Email (Login)", op.get_email())
                fone = st.text_input("Novo Telefone", op.get_fone())
                senha = st.text_input("Nova Senha (deixe vazio para manter a atual)", type="password") 
                
                submitted = st.form_submit_button("Atualizar Cliente")

                if submitted:
                    senha_final = senha if senha else op.get_senha()
                    try:
                        View.cliente_atualizar(op.get_id(), nome, email, fone, senha_final)
                        st.success(f"Cliente '{nome}' atualizado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao atualizar: {e}")

    @staticmethod
    def excluir():
        st.subheader("Excluir Cliente")
        clientes = View.cliente_listar()
        
        opcoes = {f"{c.get_nome()} ({c.get_email()}) - ID: {c.get_id()}": c for c in clientes}
        selecionado_str = st.selectbox("Selecione o cliente para excluir", list(opcoes.keys()))

        if selecionado_str:
            op: Cliente = opcoes[selecionado_str]
            
            if st.button(f"Confirmar Exclusão de {op.get_nome()}"):
                try:
                    View.cliente_excluir(op.get_id())
                    st.success(f"Cliente '{op.get_nome()}' excluído com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao excluir: {e}")

    @staticmethod
    def listar():
        st.subheader("Lista de Clientes")
        clientes = View.cliente_listar()
        
        if not clientes:
            st.info("Nenhum cliente cadastrado.")
            return

        dados_tabela = [{"ID": c.get_id(), "Nome": c.get_nome(), "Email": c.get_email(), "Telefone": c.get_fone()} for c in clientes]
        st.dataframe(dados_tabela, use_container_width=True)

    @staticmethod
    def main():
        st.title("Gerenciamento de Clientes")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Cadastrar", "Listar", "Atualizar", "Excluir"])
        
        with tab1: ManterClienteUI.cadastrar()
        with tab2: ManterClienteUI.listar()
        with tab3: ManterClienteUI.atualizar()
        with tab4: ManterClienteUI.excluir()
