import streamlit as st
from views import View
from models.profissional import Profissional

class ManterProfissionalUI:
    
    @staticmethod
    def cadastrar():
        st.subheader("Cadastrar Novo Profissional")
        
        with st.form("form_profissional_cadastro"):
            nome = st.text_input("Nome")
            especialidade = st.text_input("Especialidade")
            conselho = st.text_input("Conselho")  # Corrigido para ter "conselho"
            email = st.text_input("Email (Login)")
            senha = st.text_input("Senha", type="password")
            
            submitted = st.form_submit_button("Cadastrar Profissional")

            if submitted:
                try:
                    View.profissional_inserir(nome, especialidade, conselho, email, senha)  
                    st.success(f"Profissional '{nome}' cadastrado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao cadastrar: {e}")

    @staticmethod
    def atualizar():
        st.subheader("Atualizar Profissional")
        profissionais = View.profissional_listar()
        
        opcoes = {f"{p.get_nome()} ({p.get_especialidade()}) - ID: {p.get_id()}": p for p in profissionais}
        selecionado_str = st.selectbox("Selecione o profissional para atualizar", list(opcoes.keys()))
        
        if selecionado_str:
            op: Profissional = opcoes[selecionado_str]
            
            with st.form("form_profissional_atualizar"):
                nome = st.text_input("Novo Nome", op.get_nome())
                especialidade = st.text_input("Nova Especialidade", op.get_especialidade()) 
                conselho = st.text_input("Novo Conselho", op.get_conselho())  # Corrigido o label para ficar consistente
                email = st.text_input("Novo Email (Login)", op.get_email())
                senha = st.text_input("Nova Senha (deixe vazio para manter a atual)", type="password") 
                
                submitted = st.form_submit_button("Atualizar Profissional")

                if submitted:
                    senha_final = senha if senha else op.get_senha()
                    try:
                        View.profissional_atualizar(op.get_id(), nome, especialidade, conselho, email, senha_final)
                        st.success(f"Profissional '{nome}' atualizado com sucesso!")
                        st.set_query_params(refresh="true")
                    except Exception as e:
                        st.error(f"Erro ao atualizar: {e}")

    @staticmethod
    def excluir():
        st.subheader("Excluir Profissional")
        profissionais = View.profissional_listar()
        
        opcoes = {f"{p.get_nome()} ({p.get_especialidade()}) - ID: {p.get_id()}": p for p in profissionais}
        selecionado_str = st.selectbox("Selecione o profissional para excluir", list(opcoes.keys()))

        if selecionado_str:
            op: Profissional = opcoes[selecionado_str]
            
            if st.button(f"Confirmar Exclusão de {op.get_nome()}"):
                try:
                    View.profissional_excluir(op.get_id())
                    st.success(f"Profissional '{op.get_nome()}' excluído com sucesso!")
                    st.set_query_params(refresh="true")
                except Exception as e:
                    st.error(f"Erro ao excluir: {e}")

    @staticmethod
    def listar():
        st.subheader("Lista de Profissionais")
        profissionais = View.profissional_listar()
        
        if not profissionais:
            st.info("Nenhum profissional cadastrado.")
            return

        dados_tabela = [
            {
                "ID": p.get_id(),
                "Nome": p.get_nome(),
                "Especialidade": p.get_especialidade(),
                "Conselho": p.get_conselho(),  # Corrigido para mostrar "Conselho" corretamente
                "Email": p.get_email()
            } 
            for p in profissionais
        ]
        st.dataframe(dados_tabela, use_container_width=True)

    @staticmethod
    def main():
        st.title("Gerenciamento de Profissionais")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Cadastrar", "Listar", "Atualizar", "Excluir"])
        
        with tab1:
            ManterProfissionalUI.cadastrar()
        with tab2:
            ManterProfissionalUI.listar()
        with tab3:
            ManterProfissionalUI.atualizar()
        with tab4:
            ManterProfissionalUI.excluir()
