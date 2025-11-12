import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
from pathlib import Path
from models.profissional import ProfissionalDAO, Profissional

BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_HORARIOS = BASE_DIR / "horarios.json"


def carregar_json(caminho):
    """Carrega JSON e converte para DataFrame."""
    colunas = ['id', 'data', 'confirmado', 'cliente', 'serviço', 'profissional_id', 'profissional_nome']
    if not caminho.exists():
        return pd.DataFrame(columns=colunas)
    with open(caminho, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            df = pd.DataFrame(data)
            for c in colunas:
                if c not in df.columns:
                    df[c] = None
            return df[colunas]
        except json.JSONDecodeError:
            return pd.DataFrame(columns=colunas)


def salvar_json(caminho, df):
    """Salva DataFrame como JSON."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, indent=4, ensure_ascii=False)


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

        agenda = carregar_json(ARQUIVO_HORARIOS)
        next_id = (agenda["id"].max() + 1) if not agenda.empty else 1

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
                    linhas_novas = []
                    while dt_inicio <= dt_fim:
                        linhas_novas.append({
                            "id": int(next_id),
                            "data": dt_inicio.strftime("%d/%m/%Y %H:%M"),
                            "confirmado": False,
                            "cliente": None,
                            "serviço": None,
                            "profissional_id": int(profissional_id),
                            "profissional_nome": profissional_nome
                        })
                        next_id += 1
                        dt_inicio += delta

                    novos_horarios = pd.DataFrame(linhas_novas)
                    agenda = pd.concat([agenda, novos_horarios], ignore_index=True)
                    salvar_json(ARQUIVO_HORARIOS, agenda)
                    st.success("Agenda aberta com sucesso!")

                except ValueError as ve:
                    st.error(f"Erro de validação: {ve}")
                except Exception as e:
                    st.error(f"Erro ao criar horários: {e}")
