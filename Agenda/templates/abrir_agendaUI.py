import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
from models.profissional import ProfissionalDAO, Profissional
from pathlib import Path

DATA_DIR = Path("data")
HORARIOS_FILE = DATA_DIR / "horarios.json"

def carregar_json(caminho):
    """Carrega JSON e converte para DataFrame."""
    if not caminho.exists():
        return pd.DataFrame(columns=['id', 'data', 'confirmado', 'cliente', 'serviço', 'profissional'])
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
        return pd.DataFrame(dados)

def salvar_json(caminho, df):
    """Salva DataFrame como JSON."""
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, indent=4, ensure_ascii=False)

class AbrirAgendaUI:

    @staticmethod
    def main(profissional_info):
        """Interface para abrir horários na agenda de um profissional."""

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

        DATA_DIR.mkdir(exist_ok=True)
        agenda = carregar_json(HORARIOS_FILE)
        next_id = (agenda["id"].max() + 1) if not agenda.empty else 1

        st.title("Abrir Minha Agenda")

        with st.form("abrir_agenda_form"):
            data = st.date_input("Informe a data (dd/mm/aaaa)", datetime.today())
            hora_inicial = st.time_input("Horário inicial", datetime.strptime("09:00", "%H:%M").time())
            hora_final = st.time_input("Horário final", datetime.strptime("12:00", "%H:%M").time())
            intervalo = st.number_input("Intervalo (minutos)", min_value=1, value=30)
            submitted = st.form_submit_button("Abrir Agenda")

            if submitted:
                try:
                    dt_inicio = datetime.combine(data, hora_inicial)
                    dt_fim = datetime.combine(data, hora_final)
                    if dt_fim <= dt_inicio:
                        raise ValueError("O horário final deve ser posterior ao inicial.")
                    if intervalo <= 0:
                        raise ValueError("O intervalo deve ser maior que zero.")
                    if dt_inicio.year < 2025:
                        raise ValueError("Não é permitido abrir agenda antes de 2025.")

                    delta = timedelta(minutes=intervalo)
                    linhas_novas = []
                    while dt_inicio <= dt_fim:
                        linhas_novas.append({
                            'id': int(next_id),
                            'data': dt_inicio.strftime("%d/%m/%Y %H:%M"),
                            'confirmado': False,
                            'cliente': None,
                            'serviço': None,
                            'profissional': str(profissional_nome)
                        })
                        next_id += 1
                        dt_inicio += delta

                    novos_horarios = pd.DataFrame(linhas_novas)
                    agenda = pd.concat([agenda, novos_horarios], ignore_index=True)
                    salvar_json(HORARIOS_FILE, agenda)


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

        agenda_view = agenda.copy()
        if 'profissional' in agenda_view.columns:
            agenda_view['profissional'] = agenda_view['profissional'].apply(_garante_nome_profissional)

        st.subheader("Cadastro de Horários")
        st.dataframe(agenda_view[['id', 'data', 'confirmado', 'cliente', 'serviço', 'profissional']], use_container_width=True)
