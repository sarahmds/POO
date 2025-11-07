# index.py
import streamlit as st
from templates.loginUI import LoginUI, carregar_usuario, logout
from templates.abrircontaUI import AbrirContaUI
from templates.perfilclienteUI import PerfilClienteUI
from templates.PerfilProfissionalUI import PerfilProfissionalUI
from templates.manterclienteUI import ManterClienteUI
from templates.manterprofissionalUI import ManterProfissionalUI
from templates.manterservicoUI import ManterServicoUI
from templates.manterhorarioUI import ManterHorarioUI
from templates.abrir_agendaUI import AbrirAgendaUI
from templates.visualizar_minha_agenda_UI import VisualizarMinhaAgendaUI
from templates.perfiladminUI import PerfiladminUI
from views import View

class IndexUI:

    @staticmethod
    def sidebar():
        """Renderiza o menu lateral baseado no usuário logado."""
        usuario = carregar_usuario()
        if usuario is None:
            IndexUI.menu_visitante()
            return

        st.sidebar.write(f"Bem-vindo(a), {usuario['nome']}")
        tipo = usuario["tipo"]

        # Menu baseado no tipo
        if tipo == "admin":
            IndexUI.menu_admin()
        elif tipo == "profissional":
            IndexUI.menu_profissional(usuario["id"])
        else:
            IndexUI.menu_cliente(usuario["id"])

        # Botão Sair no final
        if st.sidebar.button("Sair"):
            logout()
            # Força atualização da página
            st.query_params = {}
            return

    @staticmethod
    def menu_visitante():
        """Menu para visitantes (não logados)."""
        op = st.sidebar.selectbox("Menu", ["Entrar no Sistema", "Abrir Conta"])
        if op == "Entrar no Sistema":
            LoginUI.main()
        elif op == "Abrir Conta":
            AbrirContaUI.main()

    @staticmethod
    def menu_cliente(cliente_id: int):
        op = st.sidebar.selectbox("Menu", [
            "Meus Dados",
            "Agendar Serviço",
            "Meus Serviços",
            "Relatório de Profissionais"
        ])
        if op == "Meus Dados":
            PerfilClienteUI.main()
        elif op == "Agendar Serviço":
            from templates.agendar_servico_UI import AgendarServicoUI
            AgendarServicoUI.main(cliente_id)
        elif op == "Meus Serviços":
            from templates.visualizar_meus_servicos_UI import VisualizarMeusServicosUI
            VisualizarMeusServicosUI.main(cliente_id)
        elif op == "Relatório de Profissionais":
            from templates.relatorio_profissionais_UI import RelatorioProfissionaisUI
            RelatorioProfissionaisUI.main()

    @staticmethod
    def menu_profissional(profissional_id: int):
        op = st.sidebar.selectbox("Menu", [
            "Meus Dados",
            "Abrir Minha Agenda",
            "Visualizar Minha Agenda",
            "Confirmar Serviço",
            "Relatório de Profissionais"
        ])
        if op == "Meus Dados":
            PerfilProfissionalUI.main()
        elif op == "Abrir Minha Agenda":
            AbrirAgendaUI.main(profissional_id)
        elif op == "Visualizar Minha Agenda":
            VisualizarMinhaAgendaUI.main(profissional_id)
        elif op == "Confirmar Serviço":
            from templates.confirmar_servico_UI import ConfirmarServicoUI
            ConfirmarServicoUI.main(profissional_id)
        elif op == "Relatório de Profissionais":
            from templates.relatorio_profissionais_UI import RelatorioProfissionaisUI
            RelatorioProfissionaisUI.main()

    @staticmethod
    def menu_admin():
        op = st.sidebar.selectbox("Menu", [
            "Cadastro de Clientes",
            "Cadastro de Profissionais",
            "Cadastro de Serviços",
            "Cadastro de Horários",
            "Relatório de Profissionais",
            "Meus Dados"
        ])
        if op == "Cadastro de Clientes":
            ManterClienteUI.main()
        elif op == "Cadastro de Profissionais":
            ManterProfissionalUI.main()
        elif op == "Cadastro de Serviços":
            ManterServicoUI.main()
        elif op == "Cadastro de Horários":
            ManterHorarioUI.main()
        elif op == "Relatório de Profissionais":
            from templates.relatorio_profissionais_UI import RelatorioProfissionaisUI
            RelatorioProfissionaisUI.main()
        elif op == "Meus Dados":
            PerfiladminUI.main()

    @staticmethod
    def main():
        st.title("Sistema de Agendamento")
        # Garante que o admin exista
        View.cliente_criar_admin()
        IndexUI.sidebar()


if __name__ == "__main__":
    IndexUI.main()
