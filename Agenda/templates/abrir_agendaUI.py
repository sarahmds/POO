import streamlit as st
from datetime import datetime, timedelta
from models.profissional import ProfissionalDAO, Profissional
from views import View

class AbrirAgendaUI:

    @staticmethod
    def main(profissional_info):
        """Interface para o profissional abrir novos horários na agenda."""

        profissional_id = None
        profissional_nome = None
        try:
            if isinstance(profissional_info, int):
                p = ProfissionalDAO.listar_id(profissional_info)
                if p:
                    profissional_id = p.get_id()
                    profissional_nome = p.get_nome()
            elif isinstance(profissional_info, Profissional):
                profissional_id = profissional_info.get_id()
                profissional_nome = profissional_info.get_nome()
        except Exception:
            pass

        if not profissional_id:
            st.error("Profissional inválido ou não encontrado.")
            return

        st.title("Abrir Agenda")

        with st.form("abrir_agenda_form"):
            data = st.date_input("Data", datetime.today())
            hora_inicial = st.time_input("Horário inicial", datetime.strptime("09:00", "%H:%M").time())
            hora_final = st.time_input("Horário final", datetime.strptime("12:00", "%H:%M").time())
            intervalo = st.number_input("Intervalo (minutos)", min_value=5, value=30)
            submitted = st.form_submit_button("Abrir Agenda")

            if submitted:
                try:
                    dt_inicio = datetime.combine(data, hora_inicial)
                    dt_fim = datetime.combine(data, hora_final)

                    if dt_fim <= dt_inicio:
                        raise ValueError("O horário final deve ser posterior ao inicial.")

                    delta = timedelta(minutes=intervalo)
                    count = 0

                    while dt_inicio <= dt_fim:
                        View.horario_inserir(
                            data=dt_inicio,  # datetime real
                            confirmado=False,
                            id_cliente=None,
                            id_servico=None,
                            id_profissional=profissional_id
                        )
                        count += 1
                        dt_inicio += delta

                    st.success(f"{count} horários adicionados à agenda de {profissional_nome}!")

                except ValueError as ve:
                    st.error(f"Erro de validação: {ve}")
                except Exception as e:
                    st.error(f"Erro ao criar horários: {e}")
