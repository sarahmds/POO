import streamlit as st
import time
import auth

class ManterProfissionalComContaUI:
    def main():
        st.header("Cadastro de Profissionais (com conta)")
        nome = st.text_input("Nome do profissional")
        profissao = st.text_input("Profissão")
        email = st.text_input("E-mail (para login)")
        senha = st.text_input("Senha (login)", type="password")
        if st.button("Inserir"):
            if not nome or not profissao:
                st.error("Nome e profissão são obrigatórios")
                return
            auth.profissional_inserir_raw(nome, profissao, email, senha)
            st.success("Profissional inserido com sucesso")
            time.sleep(1)
            st.experimental_rerun()

        st.subheader("Profissionais cadastrados")
        lista = auth.profissional_listar_objs()
        if not lista:
            st.write("Nenhum profissional cadastrado")
        else:
            for p in lista:
                st.write(f'{p.get("id")} - {p.get("nome")} - {p.get("profissao")} - {p.get("email","")}')
