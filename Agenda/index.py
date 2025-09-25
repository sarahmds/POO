from templates.manterclienteUI import ManterClienteUI
from templates.manterservicoUI import ManterServicoUI
from templates.manterhorarioUI import ManterHorarioUI
from templates.manterprofissionalUI import ManterProfissionalUI
import streamlit as st

class IndexUI:
    def menu_admin():
        op = st.sidebar.selectbox("Menu", [
            "Cadastro de Clientes",
            "Cadastro de Serviços",
            "Cadastro de Horários",
            "Cadastro de Profissionais"
        ])
        if op == "Cadastro de Clientes": ManterClienteUI.main()
        if op == "Cadastro de Serviços": ManterServicoUI.main()
        if op == "Cadastro de Horários": ManterHorarioUI.main()
        if op == "Cadastro de Profissionais": ManterProfissionalUI.main()

    def sidebar(): IndexUI.menu_admin()
    def main(): IndexUI.sidebar()

IndexUI.main()
