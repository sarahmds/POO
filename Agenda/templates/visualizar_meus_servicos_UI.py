import streamlit as st
import pandas as pd
import json
from pathlib import Path
from models.profissional import ProfissionalDAO
from models.servico import ServicoDAO

DATA_DIR = Path("data")
AGENDA_FILE = DATA_DIR / "horarios.json"


class VisualizarMeusServicosUI:

    @staticmethod
    def main(cliente_id: int):
        """Interface para o cliente visualizar seus serviços agendados."""

        st.title("Meus Serviços")

        try:
            if not AGENDA_FILE.exists():
                st.warning("Nenhum serviço encontrado. Nenhum horário foi agendado ainda.")
                return

            with open(AGENDA_FILE, "r", encoding="utf-8") as f:
                agenda_data = json.load(f)

            if not agenda_data:
                st.info("Nenhum serviço encontrado.")
                return

            df = pd.DataFrame(agenda_data)
            if df.empty:
                st.info("Nenhum serviço encontrado.")
                return

            # Filtro por cliente (aceita int ou string)
            df_cliente = df[
                (df["cliente"] == cliente_id) |
                (df["cliente"].astype(str) == str(cliente_id))
            ].copy()

            if df_cliente.empty:
                st.info("Você ainda não possui serviços agendados.")
                return

            # Converter IDs em nomes legíveis
            def get_nome_profissional(id_):
                try:
                    p = ProfissionalDAO.listar_id(int(id_))
                    return p.get_nome() if p else str(id_)
                except:
                    return str(id_)

            def get_nome_servico(id_):
                try:
                    s = ServicoDAO.listar_id(int(id_))
                    return s.get_descricao() if s else str(id_)
                except:
                    return str(id_)

            df_cliente["profissional"] = df_cliente["profissional"].apply(get_nome_profissional)
            df_cliente["serviço"] = df_cliente["serviço"].apply(get_nome_servico)

            # Selecionar colunas relevantes
            colunas = ["id", "data", "confirmado", "serviço", "profissional"]
            df_cliente = df_cliente[colunas]

            st.data_editor(
                df_cliente,
                hide_index=True,
                disabled=True,
                column_config={
                    "id": st.column_config.Column("ID"),
                    "data": st.column_config.Column("Data"),
                    "confirmado": st.column_config.CheckboxColumn("Confirmado", default=False),
                    "serviço": st.column_config.Column("Serviço"),
                    "profissional": st.column_config.Column("Profissional"),
                },
                use_container_width=True,
            )

        except Exception as e:
            st.error(f"Erro ao carregar serviços: {e}")
