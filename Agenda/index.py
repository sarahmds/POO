from templates.manterclienteUI import ManterClienteUI
from templates.manterservicoUI import ManterServicoUI
from templates.manterhorarioUI import ManterHorarioUI
import streamlit as st

class IndexUI:

    @staticmethod
    def menu_admin():
        op = st.sidebar.selectbox(
            "Menu",
            ["Cadastro de Clientes", "Cadastro de Serviços", "Cadastro de Horários"]
        )
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
        ManterClienteUI.main()

IndexUI.main()


if __name__ == "__main__":
    IndexUI.main()


