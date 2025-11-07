import streamlit as st
import pandas as pd
import json
from pathlib import Path

DATA_DIR = Path("data")
AGENDA_FILE = DATA_DIR / "agenda.json"


class VisualizarMeusServicosUI:

    @staticmethod
    def main(cliente_id: int):
        """Interface para o cliente visualizar seus serviços agendados."""

        st.title("Meus Serviços")

        try:
            # Verifica se o arquivo de agenda existe
            if not AGENDA_FILE.exists():
                st.warning("Nenhum serviço encontrado. Nenhum horário foi agendado ainda.")
                return

            # Carrega os dados da agenda
            with open(AGENDA_FILE, "r", encoding="utf-8") as f:
                agenda_data = json.load(f)

            if not agenda_data:
                st.warning("Nenhum serviço encontrado. Nenhum horário foi agendado ainda.")
                return

            df_agenda = pd.DataFrame(agenda_data)
            if df_agenda.empty:
                st.warning("Nenhum serviço encontrado. Nenhum horário foi agendado ainda.")
                return

            # Filtra serviços do cliente logado
            df_cliente = df_agenda[df_agenda["cliente"] == cliente_id].copy()

            if df_cliente.empty:
                st.info("Você ainda não possui serviços agendados.")
                return

            # Seleciona colunas relevantes
            colunas = ["id", "data", "confirmado", "serviço", "profissional"]
            df_cliente = df_cliente[colunas]

            # Exibe tabela em formato editável (somente leitura)
            st.data_editor(
                df_cliente,
                hide_index=False,
                disabled=True,
                column_config={
                    "id": st.column_config.Column("ID", width="small"),
                    "data": st.column_config.Column("Data", width="medium"),
                    "confirmado": st.column_config.CheckboxColumn("Confirmado", default=False),
                    "serviço": st.column_config.Column("Serviço", width="medium"),
                    "profissional": st.column_config.Column("Profissional", width="medium"),
                },
                use_container_width=True,
            )

        except Exception as e:
            st.error(f"Erro ao carregar serviços: {e}")
