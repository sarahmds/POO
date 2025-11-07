import streamlit as st
import pandas as pd
import json
from pathlib import Path

DATA_DIR = Path("data")
AGENDA_FILE = DATA_DIR / "agenda.json"


class VisualizarMinhaAgendaUI:

    @staticmethod
    def main(profissional_id: int):
        """Interface para visualizar os horários do profissional logado."""

        st.title("Minha Agenda")

        try:
            # Verifica se o arquivo existe
            if not AGENDA_FILE.exists():
                st.warning("Nenhum horário encontrado. Abra sua agenda primeiro.")
                return

            # Carrega os dados da agenda
            with open(AGENDA_FILE, "r", encoding="utf-8") as f:
                agenda_data = json.load(f)

            if not agenda_data:
                st.warning("Nenhum horário encontrado. Abra sua agenda primeiro.")
                return

            df_agenda = pd.DataFrame(agenda_data)
            if df_agenda.empty:
                st.warning("Nenhum horário encontrado. Abra sua agenda primeiro.")
                return

            # Filtra horários do profissional logado
            df_prof = df_agenda[df_agenda["profissional"] == profissional_id].copy()

            if df_prof.empty:
                st.info("Nenhum horário cadastrado para este profissional.")
                return

            # Seleciona e exibe colunas principais
            df_prof = df_prof[["id", "data", "confirmado", "cliente", "serviço"]]

            st.data_editor(
                df_prof,
                hide_index=True,
                disabled=True,
                column_config={
                    "id": st.column_config.Column("ID", width="small"),
                    "data": st.column_config.Column("Data", width="medium"),
                    "confirmado": st.column_config.CheckboxColumn("Confirmado", default=False),
                    "cliente": st.column_config.Column("Cliente", width="medium"),
                    "serviço": st.column_config.Column("Serviço", width="medium"),
                },
                use_container_width=True,
            )

        except Exception as e:
            st.error(f"Erro ao carregar agenda: {e}")
