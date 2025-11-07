import streamlit as st
from views import View
from models.profissional import Profissional

class ManterProfissionalUI:
    """Interface de usuário para o CRUD de Profissionais (Admin)."""

    @staticmethod
    def cadastrar():
        st.subheader("Cadastrar Novo Profissional")
        
        with st.form("form_profissional_cadastro"):
            nome = st.text_input("Nome")
            especialidade = st.text_input("Especialidade")
            conselho = st.text_input("Conselho")
            email = st.text_input("Email (Login)")
            senha = st.text_input("Senha", type="password")

            submitted = st.form_submit_button("Cadastrar Profissional")

            if submitted:
                try:
                    if not nome or not email or not senha:
                        raise ValueError("Nome, e-mail e senha são obrigatórios.")

                    View.profissional_inserir(nome, especialidade, conselho, email, senha)
                    st.rerun()
                except ValueError as ve:
                    st.error(f"Erro de validação: {ve}")
                except Exception as e:
                    st.error(f"Erro ao cadastrar profissional: {e}")

    @staticmethod
    def atualizar():
        st.subheader("Atualizar Profissional")
        try:
            profissionais = View.profissional_listar()
            if not profissionais:
                st.info("Nenhum profissional cadastrado.")
                return

            opcoes = {f"{p.get_nome()} ({p.get_especialidade() or 'Sem especialidade'}) - ID: {p.get_id()}": p for p in profissionais}
            selecionado_str = st.selectbox("Selecione o profissional para atualizar", list(opcoes.keys()))
            
            if selecionado_str:
                op: Profissional = opcoes[selecionado_str]
                
                with st.form("form_profissional_atualizar"):
                    nome = st.text_input("Novo Nome", op.get_nome())
                    especialidade = st.text_input("Nova Especialidade", op.get_especialidade() or "")
                    conselho = st.text_input("Novo Conselho", op.get_conselho() or "")
                    email = st.text_input("Novo Email (Login)", op.get_email())
                    senha = st.text_input("Nova Senha (deixe vazio para manter a atual)", type="password")

                    submitted = st.form_submit_button("Atualizar Profissional")

                    if submitted:
                        try:
                            if not nome or not email:
                                raise ValueError("Nome e e-mail são obrigatórios.")

                            senha_final = senha if senha else op.get_senha()
                            View.profissional_atualizar(op.get_id(), nome, especialidade, conselho, email, senha_final)

                            st.rerun()
                        except ValueError as ve:
                            st.error(f"Erro de validação: {ve}")
                        except Exception as e:
                            st.error(f"Erro ao atualizar profissional: {e}")
        except Exception as e:
            st.error(f"Erro ao carregar lista de profissionais: {e}")

    @staticmethod
    def excluir():
        st.subheader("Excluir Profissional")
        try:
            profissionais = View.profissional_listar()
            if not profissionais:
                st.info("Nenhum profissional cadastrado.")
                return

            opcoes = {f"{p.get_nome()} ({p.get_especialidade() or 'Sem especialidade'}) - ID: {p.get_id()}": p for p in profissionais}
            selecionado_str = st.selectbox("Selecione o profissional para excluir", list(opcoes.keys()))

            if selecionado_str:
                op: Profissional = opcoes[selecionado_str]
                
                if st.button(f"Confirmar Exclusão de {op.get_nome()}"):
                    try:
                        View.profissional_excluir(op.get_id())
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao excluir profissional: {e}")
        except Exception as e:
            st.error(f"Erro ao carregar dados para exclusão: {e}")

    @staticmethod
    def listar():
        st.subheader("Lista de Profissionais")
        try:
            profissionais = View.profissional_listar()
            if not profissionais:
                st.info("Nenhum profissional cadastrado.")
                return

            dados_tabela = [
                {
                    "ID": p.get_id(),
                    "Nome": p.get_nome(),
                    "Especialidade": p.get_especialidade() or "—",
                    "Conselho": p.get_conselho() or "—",
                    "Email": p.get_email()
                }
                for p in profissionais
            ]
            st.dataframe(dados_tabela, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao listar profissionais: {e}")

    @staticmethod
    def main():
        st.title("Gerenciamento de Profissionais")
        try:
            tab1, tab2, tab3, tab4 = st.tabs(["Cadastrar", "Listar", "Atualizar", "Excluir"])
            
            with tab1:
                ManterProfissionalUI.cadastrar()
            with tab2:
                ManterProfissionalUI.listar()
            with tab3:
                ManterProfissionalUI.atualizar()
            with tab4:
                ManterProfissionalUI.excluir()
        except Exception as e:
            st.error(f"Erro ao carregar interface de profissionais: {e}")
