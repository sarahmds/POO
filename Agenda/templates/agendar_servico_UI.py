import streamlit as st
from views import View
from models.profissional import ProfissionalDAO

class AgendarServicoUI:

    @staticmethod
    def main(cliente_id: int):
        st.title("Agendar Serviço")

        # Lista todos os horários disponíveis (id_cliente == None)
        horarios_disponiveis = View.horario_listar_disponiveis()

        if not horarios_disponiveis:
            st.warning("Nenhum horário disponível no momento.")
            return

        # Função para exibir o horário e o nome do profissional
        def formatar_horario(h):
            prof = ProfissionalDAO.listar_id(h.get_id_profissional())
            nome_prof = prof.get_nome() if prof else f"ID {h.get_id_profissional()}"
            return f"{h.get_data().strftime('%d/%m/%Y %H:%M')} com {nome_prof}"

        opcao = st.selectbox(
            "Selecione um horário disponível:",
            options=horarios_disponiveis,
            format_func=formatar_horario
        )

        # Lista de serviços disponíveis
        servicos = View.servico_listar()
        if not servicos:
            st.error("Nenhum serviço cadastrado.")
            return

        servico_opcao = st.selectbox(
            "Selecione o serviço desejado:",
            options=servicos,
            format_func=lambda s: s.get_descricao()
        )

        # Confirmar agendamento
        if st.button("Confirmar Agendamento"):
            h = opcao
            h.set_id_cliente(cliente_id)
            h.set_id_servico(servico_opcao.get_id())
            h.set_confirmado(False)
            View.horario_atualizar(
                h.get_id(),
                h.get_data(),
                h.get_confirmado(),
                h.get_id_cliente(),
                h.get_id_servico(),
                h.get_id_profissional()
            )
            st.success("Serviço agendado com sucesso!")
