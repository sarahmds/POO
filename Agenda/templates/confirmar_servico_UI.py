import streamlit as st
import pandas as pd

class ConfirmarServicoUI:

    @staticmethod
    def main(profissional_id: int):
        """Interface para o profissional confirmar serviços agendados."""

        st.title("Confirmar Serviço")

        if 'agenda' not in st.session_state or st.session_state.agenda.empty:
            st.warning("Nenhum horário encontrado. Abra sua agenda primeiro.")
            return

        df_profissional = st.session_state.agenda[
            (st.session_state.agenda['profissional'] == profissional_id) &
            (st.session_state.agenda['cliente'].notna())
        ].copy()

        if df_profissional.empty:
            st.info("Nenhum serviço agendado por clientes para confirmar.")
            return

        opcoes_horarios = [
            f"{row['id']} - {row['data'].strftime('%d/%m/%Y %H:%M')} - {row['confirmado']}"
            for _, row in df_profissional.iterrows()
        ]

        horario_escolhido = st.selectbox("Informe o horário", opcoes_horarios)

        horario_id = int(horario_escolhido.split(" - ")[0])

        horario = df_profissional[df_profissional["id"] == horario_id].iloc[0]

        clientes = st.session_state.agenda['cliente'].dropna().unique()

        if len(clientes) > 0:
            cliente_opcoes = [str(c) for c in clientes]
            cliente_selecionado = st.selectbox("Cliente", cliente_opcoes)
        else:
            st.info("Nenhum cliente agendado.")
            return

        if st.button("Confirmar"):
            idx = st.session_state.agenda[
                st.session_state.agenda["id"] == horario_id
            ].index[0]

            st.session_state.agenda.at[idx, "confirmado"] = True

            st.success("Serviço confirmado com sucesso!")

            st.dataframe(st.session_state.agenda[
                st.session_state.agenda["profissional"] == profissional_id
            ][["id", "data", "confirmado", "cliente", "serviço"]])
