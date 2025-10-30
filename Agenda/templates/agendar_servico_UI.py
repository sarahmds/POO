import streamlit as st
import pandas as pd
from views import View

class AgendarServicoUI:

    @staticmethod
    def main(cliente_id: int):
        st.title("Agendar Serviço")

        if 'agenda' not in st.session_state or st.session_state.agenda.empty:
            st.warning("Nenhum horário disponível para agendamento.")
            return

        df_disponivel = st.session_state.agenda[
            st.session_state.agenda['cliente'].isnull()
        ].copy()

        if df_disponivel.empty:
            st.info("Nenhum horário disponível no momento.")
            return

        # Mostrar horários disponíveis
        df_disponivel['data_str'] = df_disponivel['data'].astype(str)
        opcao = st.selectbox(
            "Selecione um horário disponível:",
            options=df_disponivel.index,
            format_func=lambda idx: f"{df_disponivel.loc[idx, 'data']} com Profissional {df_disponivel.loc[idx, 'profissional']}"
        )

        servicos = View.servico_listar()
        if not servicos:
            st.error("Nenhum serviço cadastrado.")
            return

        servico_opcao = st.selectbox(
            "Selecione o serviço desejado:",
            options=servicos,
            format_func=lambda s: s.get_descricao()
        )

        if st.button("Confirmar Agendamento"):
            st.session_state.agenda.at[opcao, 'cliente'] = cliente_id
            st.session_state.agenda.at[opcao, 'serviço'] = servico_opcao.get_descricao()
            st.session_state.agenda.at[opcao, 'confirmado'] = False

            st.success("Serviço agendado com sucesso!")
