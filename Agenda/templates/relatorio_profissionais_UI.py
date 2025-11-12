import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from pathlib import Path
from views import View

BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_HORARIOS = BASE_DIR / "horarios.json"


class RelatorioProfissionaisUI:

    @staticmethod
    def main():
        st.header("Relatório de Serviços Confirmados por Profissional")

        try:
            profissionais = View.profissional_listar()
            if not profissionais:
                st.warning("Não há profissionais cadastrados.")
                return

            df_profissionais = pd.DataFrame([
                {'id': p.get_id(), 'nome': p.get_nome()}
                for p in profissionais
            ])

            if not ARQUIVO_HORARIOS.exists():
                st.warning("Nenhum serviço agendado ainda.")
                return

            try:
                with open(ARQUIVO_HORARIOS, "r", encoding="utf-8") as f:
                    agenda_data = json.load(f)
            except json.JSONDecodeError:
                st.error("Erro ao ler o arquivo de horários.")
                return

            if not agenda_data:
                st.warning("Nenhum serviço agendado ainda.")
                return

            df_agenda = pd.DataFrame(agenda_data)
            if df_agenda.empty:
                st.warning("Nenhum serviço agendado ainda.")
                return

            df_agenda.rename(columns={
                "id_profissional": "profissional",
                "id_cliente": "cliente",
                "id_servico": "servico"
            }, inplace=True)

            if "confirmado" not in df_agenda.columns:
                df_agenda["confirmado"] = False
            else:
                df_agenda["confirmado"] = df_agenda["confirmado"].apply(
                    lambda x: str(x).strip().lower() in ["true", "sim", "1"]
                )

            df_confirmados = df_agenda[df_agenda["confirmado"] == True]

            if df_confirmados.empty:
                st.info("Nenhum serviço confirmado para gerar o relatório.")
                return

            relatorio = (
                df_confirmados.groupby("profissional")
                .size()
                .reset_index(name="quantidade")
            )

            relatorio = df_profissionais.merge(
                relatorio, how="left", left_on="id", right_on="profissional"
            )

            relatorio["quantidade"] = relatorio["quantidade"].fillna(0).astype(int)

            total = relatorio["quantidade"].sum()
            if total == 0:
                st.info("Nenhum serviço confirmado para gerar o relatório.")
                return

            relatorio["porcentagem"] = 100 * relatorio["quantidade"] / total


            relatorio_grafico = relatorio[relatorio["quantidade"] > 0]

            if relatorio_grafico.empty:
                st.info("Nenhum serviço confirmado para exibir no gráfico.")
            else:
                fig, ax = plt.subplots()
                ax.pie(
                    relatorio_grafico["quantidade"],
                    labels=relatorio_grafico["nome"],
                    autopct="%1.1f%%"
                )
                ax.set_title("Porcentagem de Serviços Confirmados por Profissional")
                st.pyplot(fig)

            st.dataframe(relatorio[["nome", "quantidade", "porcentagem"]])

        except Exception as e:
            st.error(f"Erro ao gerar relatório: {e}")
