import streamlit as st
from templates.manterclienteUI import ManterClienteUI
from templates.manterservicoUI import ManterServicoUI

class IndexUI:
    def main():
        st.sidebar.title("Menu")
        opcao = st.sidebar.selectbox("Escolha uma opção", ["Clientes", "Serviços"])

        if opcao == "Clientes":
            ManterClienteUI.main()
        elif opcao == "Serviços":
            ManterServicoUI.main()

IndexUI.main()
