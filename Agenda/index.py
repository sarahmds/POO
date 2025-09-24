import streamlit as st
from templates.manterclienteUI import ManterClienteUI
from templates.manterservicoUI import ManterServicoUI
from templates.manterHorarioUI import ManterHorarioUI


class IndexUI:
    @staticmethod
    def menu_admin():
        op = st.sidebar.selectbox("Menu", [
            "Cadastro de Clientes",
            "Cadastro de Serviços",
            "Cadastro de Horários"
        ])
        if op == "Cadastro de Clientes":
            ManterClienteUI.main()
        elif op == "Cadastro de Serviços":
            ManterServicoUI.main()
        elif op == "Cadastro de Horários":
            ManterHorarioUI.main()

    @staticmethod
    def sidebar():
        IndexUI.menu_admin()

    @staticmethod
    def main():
        IndexUI.sidebar()


if __name__ == "__main__":
    IndexUI.main()
