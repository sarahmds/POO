import streamlit as st
import pandas as pd

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

        df_disponivel['data_str'] = df_disponivel['data'].astype(str)
        opcao = st.selectbox(
            "Selecione um horário disponível:",
            options=df_disponivel.index,
            format_func=lambda idx: f"{df_disponivel.loc[idx, 'data']} com {df_disponivel.loc[idx, 'profissional']}"
        )

        servico = st.text_input("Digite o serviço que deseja agendar:")

        if st.button("Confirmar Agendamento"):
            if not servico.strip():
                st.error("Você deve informar o serviço desejado.")
                return

            st.session_state.agenda.at[opcao, 'cliente'] = cliente_id
            st.session_state.agenda.at[opcao, 'serviço'] = servico
            st.session_state.agenda.at[opcao, 'confirmado'] = False

            st.success("Serviço agendado com sucesso!")
