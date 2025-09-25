import streamlit as st
import pandas as pd
from views import View
import time

class ManterProfissionalUI:
    def main():
        st.header("Cadastro de Profissionais")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterProfissionalUI.listar()
        with tab2: ManterProfissionalUI.inserir()
        with tab3: ManterProfissionalUI.atualizar()
        with tab4: ManterProfissionalUI.excluir()

    def listar():
        profissionais = View.profissional_listar()
        if len(profissionais) == 0: st.write("Nenhum profissional cadastrado")
        else:
            list_dic = [obj.to_json() for obj in profissionais]
            st.dataframe(pd.DataFrame(list_dic))

    def inserir():
        nome = st.text_input("Informe o nome")
        profissao = st.text_input("Informe a profissão")
        if st.button("Inserir"):
            View.profissional_inserir(nome, profissao)
            st.success("Profissional inserido com sucesso")
            time.sleep(2)
            st.rerun()

    def atualizar():
        profissionais = View.profissional_listar()
        if len(profissionais) == 0: st.write("Nenhum profissional cadastrado")
        else:
            op = st.selectbox("Atualização de Profissionais", profissionais)
            nome = st.text_input("Informe o novo nome", op.get_nome())
            profissao = st.text_input("Informe a nova profissão", op.get_profissao())
            if st.button("Atualizar"):
                View.profissional_atualizar(op.get_id(), nome, profissao)
                st.success("Profissional atualizado com sucesso")
                time.sleep(2)
                st.rerun()

    def excluir():
        profissionais = View.profissional_listar()
        if len(profissionais) == 0: st.write("Nenhum profissional cadastrado")
        else:
            op = st.selectbox("Exclusão de Profissionais", profissionais)
            if st.button("Excluir"):
                View.profissional_excluir(op.get_id())
                st.success("Profissional excluído com sucesso")
                time.sleep(2)
                st.rerun()
