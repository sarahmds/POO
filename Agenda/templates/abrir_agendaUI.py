import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

class AbrirAgendaUI:

    @staticmethod
    def main(profissional_nome: str):
        """Interface para abrir horários na agenda de um profissional."""

        if 'agenda' not in st.session_state:
            st.session_state.agenda = pd.DataFrame(columns=[
                'id', 'data', 'confirmado', 'cliente', 'serviço', 'profissional'
            ])
            st.session_state.next_id = 1

        st.title("Abrir Minha Agenda")

        with st.form("abrir_agenda_form"):
            data = st.date_input(
                "Informe a data no formato dd/mm/aaaa",
                datetime.today()
            )
            hora_inicial = st.time_input(
                "Informe o horário inicial no formato HH:MM",
                datetime.strptime("09:00", "%H:%M").time()
            )
            hora_final = st.time_input(
                "Informe o horário final no formato HH:MM",
                datetime.strptime("12:00", "%H:%M").time()
            )
            intervalo = st.number_input(
                "Informe o intervalo entre os horários (min)",
                min_value=1,
                value=30
            )

            submitted = st.form_submit_button("Abrir Agenda")

            if submitted:
                dt_inicio = datetime.combine(data, hora_inicial)
                dt_fim = datetime.combine(data, hora_final)
                delta = timedelta(minutes=intervalo)

                while dt_inicio <= dt_fim:
                    st.session_state.agenda.loc[st.session_state.next_id] = [
                        st.session_state.next_id,
                        dt_inicio,
                        False,
                        None,
                        None,
                        profissional_nome
                    ]
                    st.session_state.next_id += 1
                    dt_inicio += delta

                st.success("Horários adicionados com sucesso!")

        st.subheader("Cadastro de Horários")
        st.dataframe(st.session_state.agenda)
