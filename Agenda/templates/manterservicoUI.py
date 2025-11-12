import streamlit as st
import pandas as pd
from views import View
import time

class ManterServicoUI:
    """Interface de usuário para o CRUD (Manutenção) de Serviços - acesso Admin."""

    @staticmethod
    def main():
        st.header("Gerenciamento de Serviços")
        try:
            tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
            with tab1:
                ManterServicoUI.listar()
            with tab2:
                ManterServicoUI.inserir()
            with tab3:
                ManterServicoUI.atualizar()
            with tab4:
                ManterServicoUI.excluir()
        except Exception as e:
            st.error(f"Erro ao carregar interface de serviços: {e}")

    @staticmethod
    def listar():
        try:
            servicos = View.servico_listar()
            if not servicos:
                st.info("Nenhum serviço cadastrado.")
                return

            dados = [
                {
                    "ID": s.get_id(),
                    "Descrição": s.get_descricao(),
                    "Preço (R$)": f"{s.get_preco():.2f}"
                }
                for s in servicos
            ]

            df = pd.DataFrame(dados, columns=["ID", "Descrição", "Preço (R$)"])
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao listar serviços: {e}")

    @staticmethod
    def inserir():
        st.subheader("Inserir Novo Serviço")
        try:
            with st.form("form_inserir_servico"):
                descricao = st.text_input("Descrição do Serviço")
                preco = st.number_input("Preço", min_value=0.0, format="%.2f")
                submitted = st.form_submit_button("Inserir")

                if submitted:
                    if not descricao.strip():
                        st.error("A descrição do serviço é obrigatória.")
                        return

                    View.servico_inserir(descricao, preco)
                    st.success(f"Serviço '{descricao}' inserido com sucesso.")
                    time.sleep(1.5)
                    st.rerun()
        except Exception as e:
            st.error(f"Erro ao inserir serviço: {e}")

    @staticmethod
    def atualizar():
        st.subheader("Atualizar Serviço Existente")
        try:
            servicos = View.servico_listar()
            if not servicos:
                st.info("Nenhum serviço cadastrado.")
                return

            op = st.selectbox(
                "Selecione o serviço para atualizar",
                servicos,
                format_func=lambda s: f"{s.get_descricao()} (R$ {s.get_preco():.2f})"
            )

            with st.form(f"form_atualizar_{op.get_id()}"):
                descricao = st.text_input("Nova Descrição", op.get_descricao())
                preco = st.number_input("Novo Preço", min_value=0.0, value=op.get_preco(), format="%.2f")
                submitted = st.form_submit_button("Atualizar")

                if submitted:
                    if not descricao.strip():
                        st.error("A descrição do serviço é obrigatória.")
                        return

                    View.servico_atualizar(op.get_id(), descricao, preco)
                    st.success(f"Serviço '{descricao}' atualizado com sucesso.")
                    time.sleep(1.5)
                    st.rerun()
        except Exception as e:
            st.error(f"Erro ao atualizar serviço: {e}")

    @staticmethod
    def excluir():
        st.subheader("Excluir Serviço")
        try:
            servicos = View.servico_listar()
            if not servicos:
                st.info("Nenhum serviço cadastrado.")
                return

            op = st.selectbox(
                "Selecione o serviço para excluir",
                servicos,
                format_func=lambda s: f"{s.get_descricao()} (R$ {s.get_preco():.2f})"
            )

            if st.button(f"Confirmar exclusão de '{op.get_descricao()}'"):
                View.servico_excluir(op.get_id())
                st.success(f"Serviço '{op.get_descricao()}' excluído com sucesso.")
                time.sleep(1.5)
                st.rerun()
        except Exception as e:
            st.error(f"Erro ao excluir serviço: {e}")
