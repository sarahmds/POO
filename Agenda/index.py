import streamlit as st
import auth
from templates.loginUI import LoginUI
from templates.abrircontaUI import AbrirContaUI
from templates.perfilclienteUI import PerfilClienteUI
from templates.manterclienteUI import ManterClienteUI
from templates.manterservicoUI import ManterServicoUI
from templates.manterhorarioUI import ManterHorarioUI
from templates.manterprofissionalUI import ManterProfissionalUI
from templates.manterprofissional_comconta import ManterProfissionalComContaUI


def sair_do_sistema():
    if st.sidebar.button("Sair"):
        for k in ["usuario_id", "usuario_nome", "usuario_tipo"]:
            st.session_state.pop(k, None)

        st.session_state["sair"] = True


class IndexUI:

    @staticmethod
    def menu_visitante():
        op = st.sidebar.selectbox("Menu", ["Entrar no Sistema", "Abrir Conta"])
        if op == "Entrar no Sistema":
            LoginUI.main()
        elif op == "Abrir Conta":
            AbrirContaUI.main()

    @staticmethod
    def menu_cliente():
        op = st.sidebar.selectbox("Menu", ["Meus Dados"])
        if op == "Meus Dados":
            PerfilClienteUI.main()

    @staticmethod
    def menu_admin():
        op = st.sidebar.selectbox("Menu", [
            "Cadastro de Clientes",
            "Cadastro de Serviços",
            "Cadastro de Horários",
            "Cadastro de Profissionais (simples)",
            "Cadastro de Profissionais (com conta)"
        ])
        if op == "Cadastro de Clientes":
            ManterClienteUI.main()
        elif op == "Cadastro de Serviços":
            ManterServicoUI.main()
        elif op == "Cadastro de Horários":
            ManterHorarioUI.main()
        elif op == "Cadastro de Profissionais (simples)":
            ManterProfissionalUI.main()
        elif op == "Cadastro de Profissionais (com conta)":
            ManterProfissionalComContaUI.main()

    @staticmethod
    def sidebar():

        if st.session_state.get("sair", False):
            st.session_state["sair"] = False
            st.rerun()  
            return

        if "usuario_id" not in st.session_state:
            IndexUI.menu_visitante()
        else:
            admin = st.session_state.get("usuario_nome", "") == "admin"
            st.sidebar.write("Bem-vindo(a), " + st.session_state.get("usuario_nome", ""))
            if admin:
                IndexUI.menu_admin()
            else:
                IndexUI.menu_cliente()
            sair_do_sistema()

    @staticmethod
    def main():
        auth.cliente_criar_admin()
        st.title("Sistema de Agendamento")
        IndexUI.sidebar()


if __name__ == "__main__":
    IndexUI.main()

