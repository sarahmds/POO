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
                "Informe a data (dd/mm/aaaa)",
                datetime.today()
            )
            hora_inicial = st.time_input(
                "Informe o horário inicial (HH:MM)",
                datetime.strptime("09:00", "%H:%M").time()
            )
            hora_final = st.time_input(
                "Informe o horário final (HH:MM)",
                datetime.strptime("12:00", "%H:%M").time()
            )
            intervalo = st.number_input(
                "Informe o intervalo entre os horários (minutos)",
                min_value=1,
                value=30
            )

            submitted = st.form_submit_button("Abrir Agenda")

            if submitted:
                try:
                    dt_inicio = datetime.combine(data, hora_inicial)
                    dt_fim = datetime.combine(data, hora_final)

                    if dt_fim <= dt_inicio:
                        raise ValueError("O horário final deve ser posterior ao horário inicial.")
                    if intervalo <= 0:
                        raise ValueError("O intervalo deve ser maior que zero.")
                    if dt_inicio.year < 2025:
                        raise ValueError("Não é permitido abrir agenda antes do ano de 2025.")

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

                except ValueError as ve:
                    st.error(f"Erro de validação: {ve}")

                except Exception as e:
                    st.error(f"Ocorreu um erro ao criar os horários: {e}")

        st.subheader("Cadastro de Horários")
        st.dataframe(st.session_state.agenda)
