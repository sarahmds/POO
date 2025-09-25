import streamlit as st
import pandas as pd
from models.profissional import Profissional
from models.profissional_dao import ProfissionalDAO
from views import View
import time

class ManterProfissionalUI:
    def main():
        st.header("Cadastro de Profissionais")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1:
            ManterProfissionalUI.listar()
        with tab2:
            ManterProfissionalUI.inserir()
        with tab3:
            ManterProfissionalUI.atualizar()
        with tab4:
            ManterProfissionalUI.excluir()

    def listar():
        profs = ProfissionalDAO.listar()
        if len(profs) == 0:
            st.write("Nenhum profissional cadastrado")
        else:
            dic = []
            for p in profs:
                dic.append({"id": p.get_id(), "nome": p.get_nome(), "telefone": p.get_telefone()})
            df = pd.DataFrame(dic)
            st.dataframe(df)

    def inserir():
        nome = st.text_input("Nome do profissional")
        telefone = st.text_input("Telefone (opcional)")
        if st.button("Inserir"):
            p = Profissional(0, nome, telefone)
            ProfissionalDAO.inserir(p)
            st.success("Profissional inserido com sucesso")

    def atualizar():
        profs = ProfissionalDAO.listar()
        if len(profs) == 0:
            st.write("Nenhum profissional cadastrado")
            return
        op = st.selectbox("Atualizar profissional", profs)
        nome = st.text_input("Nome", op.get_nome())
        telefone = st.text_input("Telefone", op.get_telefone())
        if st.button("Atualizar"):
            p = Profissional(op.get_id(), nome, telefone)
            ProfissionalDAO.atualizar(p)
            st.success("Profissional atualizado com sucesso")

    def excluir():
        profs = ProfissionalDAO.listar()
        if len(profs) == 0:
            st.write("Nenhum profissional cadastrado")
            return
        op = st.selectbox("Excluir profissional", profs)
        if st.button("Excluir"):
            ProfissionalDAO.excluir(op)
            st.success("Profissional excluído com sucesso")
            time.sleep(1)
            st.rerun()
