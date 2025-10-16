import streamlit as st
import pandas as pd

class VisualizarMinhaAgendaUI:

    @staticmethod
    def main(profissional_id: int):
        """Interface para visualizar os horários do profissional logado."""

        st.title("Minha Agenda")

        if 'agenda' not in st.session_state or st.session_state.agenda.empty:
            st.warning("Nenhum horário encontrado. Abra sua agenda primeiro.")
            return

        df_agenda = st.session_state.agenda[
            st.session_state.agenda['profissional'] == profissional_id
        ].copy()

        if df_agenda.empty:
            st.info("Nenhum horário cadastrado para este profissional.")
            return

        df_agenda = df_agenda[['id', 'data', 'confirmado', 'cliente', 'serviço']]

        st.data_editor(
            df_agenda,
            hide_index=True,
            disabled=True,
            column_config={
                "id": st.column_config.Column("id", width="small"),
                "data": st.column_config.Column("data", width="medium"),
                "confirmado": st.column_config.CheckboxColumn("confirmado", default=False),
                "cliente": st.column_config.Column("cliente", width="medium"),
                "serviço": st.column_config.Column("serviço", width="medium"),
            },
            use_container_width=True,
        )
