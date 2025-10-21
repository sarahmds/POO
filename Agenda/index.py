import streamlit as st
import auth

from templates.loginUI import LoginUI
from templates.abrircontaUI import AbrirContaUI
from templates.perfilclienteUI import PerfilClienteUI
from templates.PerfilProfissionalUI import PerfilProfissionalUI
from templates.manterclienteUI import ManterClienteUI
from templates.manterservicoUI import ManterServicoUI
from templates.manterhorarioUI import ManterHorarioUI
from templates.manterprofissionalUI import ManterProfissionalUI
from templates.abrir_agendaUI import AbrirAgendaUI 
from templates.visualizar_minha_agenda_UI import VisualizarMinhaAgendaUI 

def sair_do_sistema():
    """Função para limpar os dados da sessão e deslogar o usuário."""
    if st.sidebar.button("Sair"):
        for k in ["usuario_id", "usuario_nome", "usuario_tipo"]:
            st.session_state.pop(k, None)
        st.session_state["sair"] = True

class IndexUI:

    @staticmethod
    def menu_visitante():
        """Menu exibido para usuários não logados."""
        op = st.sidebar.selectbox("Menu", ["Entrar no Sistema", "Abrir Conta"])
        if op == "Entrar no Sistema":
            LoginUI.main()
        elif op == "Abrir Conta":
            AbrirContaUI.main()

    @staticmethod
    def menu_cliente():
        """Menu exibido para clientes logados."""
        op = st.sidebar.selectbox("Menu", ["Meus Dados", "Agendar Serviço", "Meus Serviços"])

        cliente_id = st.session_state.get("usuario_id")

        if op == "Meus Dados":
            PerfilClienteUI.main()
        elif op == "Agendar Serviço":
            from templates.agendar_servico_UI import AgendarServicoUI
            AgendarServicoUI.main(cliente_id)
        elif op == "Meus Serviços":
            from templates.visualizar_meus_servicos_UI import VisualizarMeusServicosUI
            VisualizarMeusServicosUI.main(cliente_id)



    @staticmethod
    def menu_profissional():
        """Menu exibido para profissionais logados."""
        op = st.sidebar.selectbox("Menu", [
            "Meus Dados",
            "Abrir Minha Agenda",
            "Visualizar Minha Agenda",
            "Confirmar Serviço"
        ])

        if op == "Meus Dados":
            PerfilProfissionalUI.main()
        elif op == "Abrir Minha Agenda":
            profissional_id = st.session_state.get("usuario_id")
            AbrirAgendaUI.main(profissional_id)
        elif op == "Visualizar Minha Agenda":
            profissional_id = st.session_state.get("usuario_id")
            VisualizarMinhaAgendaUI.main(profissional_id)
        elif op == "Confirmar Serviço":
            from templates.confirmar_servico_UI import ConfirmarServicoUI
            profissional_id = st.session_state.get("usuario_id")
            ConfirmarServicoUI.main(profissional_id)

    @staticmethod
    def menu_admin():
        """Menu exibido para o administrador."""
        op = st.sidebar.selectbox("Menu", [
            "Cadastro de Clientes",
            "Cadastro de Serviços",
            "Cadastro de Horários",
            "Cadastro de Profissionais"
        ])
        if op == "Cadastro de Clientes":
            ManterClienteUI.main()
        elif op == "Cadastro de Serviços":
            ManterServicoUI.main()
        elif op == "Cadastro de Horários":
            ManterHorarioUI.main()
        elif op == "Cadastro de Profissionais":
            ManterProfissionalUI.main()

    @staticmethod
    def sidebar():
        """Controla a barra lateral e o redirecionamento baseado no estado da sessão."""
        if st.session_state.get("sair", False):
            st.session_state["sair"] = False
            st.rerun()
            return

        if "usuario_id" not in st.session_state:
            IndexUI.menu_visitante()
        else:
            tipo_usuario = st.session_state.get("usuario_tipo", "")
            st.sidebar.write("Bem-vindo(a), " + st.session_state.get("usuario_nome", ""))

            if tipo_usuario == "admin":
                IndexUI.menu_admin()
            elif tipo_usuario == "profissional":
                IndexUI.menu_profissional()
            else:
                IndexUI.menu_cliente()

            sair_do_sistema()

    @staticmethod
    def main():
        """Função principal do aplicativo Streamlit."""
        auth.cliente_criar_admin()  
        st.title("Sistema de Agendamento")
        IndexUI.sidebar()


if __name__ == "__main__":
    IndexUI.main()
