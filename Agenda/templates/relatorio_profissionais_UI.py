import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from pathlib import Path
from views import View

DATA_DIR = Path("data")
AGENDA_FILE = DATA_DIR / "agenda.json"


class RelatorioProfissionaisUI:

    @staticmethod
    def main():
        st.header("Relatório de Serviços Confirmados por Profissional")

        try:
            profissionais = View.profissional_listar()
            if not profissionais:
                st.warning("Não há profissionais cadastrados.")
                return

            df_profissionais = pd.DataFrame([{
                'id': p.get_id(),
                'nome': p.get_nome()
            } for p in profissionais])

            # Verifica se o arquivo de agenda existe
            if not AGENDA_FILE.exists():
                st.warning("Nenhum serviço agendado ainda.")
                return

            # Carrega os dados da agenda
            with open(AGENDA_FILE, "r", encoding="utf-8") as f:
                agenda_data = json.load(f)

            if not agenda_data:
                st.warning("Nenhum serviço agendado ainda.")
                return

            df_agenda = pd.DataFrame(agenda_data)
            if df_agenda.empty:
                st.warning("Nenhum serviço agendado ainda.")
                return

            # Garante a coluna 'confirmado' presente e como bool
            df_agenda["confirmado"] = df_agenda["confirmado"].fillna(False)

            # Filtra apenas serviços confirmados
            relatorio = (
                df_agenda[df_agenda["confirmado"] == True]
                .groupby("profissional")
                .size()
                .reset_index(name="quantidade")
            )

            # Junta com dados dos profissionais
            relatorio = df_profissionais.merge(
                relatorio, how="left", left_on="id", right_on="profissional"
            )
            relatorio["quantidade"] = relatorio["quantidade"].fillna(0)

            total = relatorio["quantidade"].sum()
            if total == 0:
                st.info("Nenhum serviço confirmado para gerar o relatório.")
                return

            relatorio["porcentagem"] = 100 * relatorio["quantidade"] / total

            # Gera gráfico de pizza
            fig, ax = plt.subplots()
            ax.pie(relatorio["quantidade"], labels=relatorio["nome"], autopct="%1.1f%%")
            ax.set_title("Porcentagem de Serviços Confirmados por Profissional")
            st.pyplot(fig)

            # Mostra tabela
            st.dataframe(relatorio[["nome", "quantidade", "porcentagem"]])

        except Exception as e:
            st.error(f"Erro ao gerar relatório: {e}")
