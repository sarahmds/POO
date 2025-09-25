import streamlit as st
import pandas as pd
from views import View
import time

class ManterServicoUI:
    def main():
        st.header("Cadastro de Serviços")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterServicoUI.listar()
        with tab2: ManterServicoUI.inserir()
        with tab3: ManterServicoUI.atualizar()
        with tab4: ManterServicoUI.excluir()

    def listar():
        servicos = View.servico_listar()
        if len(servicos) == 0: st.write("Nenhum serviço cadastrado")
        else:
            list_dic = []
            for obj in servicos: list_dic.append(obj.to_json())
            df = pd.DataFrame(list_dic)
            st.dataframe(df)

    def inserir():
        descricao = st.text_input("Informe a descrição do serviço")
        preco = st.number_input("Informe o preço", min_value=0.0, format="%.2f")
        if st.button("Inserir"):
            View.servico_inserir(descricao, preco)
            st.success("Serviço inserido com sucesso")
            time.sleep(2)
            st.rerun()

    def atualizar():
        servicos = View.servico_listar()
        if len(servicos) == 0: st.write("Nenhum serviço cadastrado")
        else:
            op = st.selectbox("Atualização de Serviços", servicos)
            descricao = st.text_input("Informe a nova descrição", op.get_descricao())
            preco = st.number_input("Informe o novo preço", value=op.get_preco(), format="%.2f")
            if st.button("Atualizar"):
                id = op.get_id()
                View.servico_atualizar(id, descricao, preco)
                st.success("Serviço atualizado com sucesso")
                time.sleep(2)
                st.rerun()

    def excluir():
        servicos = View.servico_listar()
        if len(servicos) == 0: st.write("Nenhum serviço cadastrado")
        else:
            op = st.selectbox("Exclusão de Serviços", servicos)
            if st.button("Excluir"):
                id = op.get_id()
                View.servico_excluir(id)
                st.success("Serviço excluído com sucesso")
                time.sleep(2)
                st.rerun()
