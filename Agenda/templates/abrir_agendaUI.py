import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from models.profissional import ProfissionalDAO, Profissional

class AbrirAgendaUI:

    @staticmethod
    def main(profissional_info):
        """Interface para abrir horários na agenda de um profissional.
           profissional_info pode ser: id (int), objeto Profissional, ou nome (str).
        """

        
        profissional_nome = None
        try:
            
            if isinstance(profissional_info, int):
                p = ProfissionalDAO.listar_id(profissional_info)
                profissional_nome = p.get_nome() if p else None
            
            elif isinstance(profissional_info, Profissional):
                profissional_nome = profissional_info.get_nome()
            
            else:
                profissional_nome = str(profissional_info).strip()
        except Exception:
            profissional_nome = None

        if not profissional_nome:
            st.error("Profissional inválido ou não encontrado.")
            return

        
        if 'agenda' not in st.session_state:
            st.session_state.agenda = pd.DataFrame(columns=[
                'id', 'data', 'confirmado', 'cliente', 'serviço', 'profissional'
            ])
            st.session_state.next_id = 1

        st.title("Abrir Minha Agenda")

        with st.form("abrir_agenda_form"):
            data = st.date_input("Informe a data (dd/mm/aaaa)", datetime.today())
            hora_inicial = st.time_input("Informe o horário inicial (HH:MM)", datetime.strptime("09:00", "%H:%M").time())
            hora_final = st.time_input("Informe o horário final (HH:MM)", datetime.strptime("12:00", "%H:%M").time())
            intervalo = st.number_input("Informe o intervalo entre os horários (minutos)", min_value=1, value=30)

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
                    linhas_novas = []
                    while dt_inicio <= dt_fim:
                        
                        linhas_novas.append({
                            'id': st.session_state.next_id,
                            'data': dt_inicio.strftime("%d/%m/%Y %H:%M"),
                            'confirmado': False,
                            'cliente': None,
                            'serviço': None,
                            'profissional': str(profissional_nome)  
                        })
                        st.session_state.next_id += 1
                        dt_inicio += delta

                    if linhas_novas:
                        st.session_state.agenda = pd.concat(
                            [st.session_state.agenda, pd.DataFrame(linhas_novas)],
                            ignore_index=True
                        )

                    st.success("Horários adicionados com sucesso!")

                except ValueError as ve:
                    st.error(f"Erro de validação: {ve}")
                except Exception as e:
                    st.error(f"Ocorreu um erro ao criar os horários: {e}")

        
        def _garante_nome_profissional(val):
            
            if val is None:
                return None
            if isinstance(val, str):
                v = val.strip()
                if v == "":
                    return None
                
                if v.isdigit():
                    p = ProfissionalDAO.listar_id(int(v))
                    return p.get_nome() if p else v
                return v
            
            try:
                if isinstance(val, int) or (isinstance(val, float) and val.is_integer()):
                    p = ProfissionalDAO.listar_id(int(val))
                    return p.get_nome() if p else str(val)
            except Exception:
                pass
            
            return str(val)

        
        agenda_view = st.session_state.agenda.copy()
        if 'profissional' in agenda_view.columns:
            agenda_view['profissional'] = agenda_view['profissional'].apply(_garante_nome_profissional)

        st.subheader("Cadastro de Horários")
        st.dataframe(agenda_view[['id', 'data', 'confirmado', 'cliente', 'serviço', 'profissional']], use_container_width=True)
