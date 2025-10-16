import streamlit as st
import pandas as pd

class VisualizarMeusServicosUI:

    @staticmethod
    def main(cliente_id: int):
        """Interface para o cliente visualizar seus serviços agendados."""

        st.title("Meus Serviços")

        # Verifica se a agenda existe no session_state
        if 'agenda' not in st.session_state or st.session_state.agenda.empty:
            st.warning("Nenhum serviço encontrado. Nenhum horário foi agendado ainda.")
            return

        # Filtra os serviços agendados para este cliente
        df_cliente = st.session_state.agenda[
            st.session_state.agenda['cliente'] == cliente_id
        ].copy()

        if df_cliente.empty:
            st.info("Você ainda não possui serviços agendados.")
            return

        # Seleciona as colunas relevantes para exibição
        df_cliente = df_cliente[['id', 'data', 'confirmado', 'serviço', 'profissional']]

        # Exibe tabela formatada (somente leitura)
        st.data_editor(
            df_cliente,
            hide_index=True,
            disabled=True,
            column_config={
                "id": st.column_config.Column("id", width="small"),
                "data": st.column_config.Column("data", width="medium"),
                "confirmado": st.column_config.CheckboxColumn("confirmado", default=False),
                "serviço": st.column_config.Column("serviço", width="medium"),
                "profissional": st.column_config.Column("profissional", width="medium"),
            },
            use_container_width=True,
        )
