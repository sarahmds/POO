import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from views import View


class RelatorioProfissionaisUI:

    @staticmethod
    def main():
        st.header("Relatório de Serviços Confirmados por Profissional")

        try:
            # 1️⃣ Lista os profissionais a partir da View
            profissionais = View.profissional_listar()
            if not profissionais:
                st.warning("Não há profissionais cadastrados.")
                return

            df_profissionais = pd.DataFrame([
                {"id": p.get_id(), "nome": p.get_nome()}
                for p in profissionais
            ])

            # 2️⃣ Lista os agendamentos a partir da View (sem ler JSON direto)
            agenda_data = View.horario_listar()
            if not agenda_data:
                st.warning("Nenhum serviço agendado ainda.")
                return

            df_agenda = pd.DataFrame([h.to_json() for h in agenda_data])
            if df_agenda.empty:
                st.warning("Nenhum serviço agendado ainda.")
                return

            # 3️⃣ Normaliza e garante colunas corretas
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

            # 4️⃣ Filtra apenas os serviços confirmados
            df_confirmados = df_agenda[df_agenda["confirmado"] == True]
            if df_confirmados.empty:
                st.info("Nenhum serviço confirmado para gerar o relatório.")
                return

            # 5️⃣ Agrupa por profissional e conta confirmações
            relatorio = (
                df_confirmados.groupby("profissional")
                .size()
                .reset_index(name="quantidade")
            )

            # 6️⃣ Junta com os nomes dos profissionais
            relatorio = df_profissionais.merge(
                relatorio, how="left", left_on="id", right_on="profissional"
            )

            relatorio["quantidade"] = relatorio["quantidade"].fillna(0).astype(int)

            total = relatorio["quantidade"].sum()
            if total == 0:
                st.info("Nenhum serviço confirmado para gerar o relatório.")
                return

            relatorio["porcentagem"] = 100 * relatorio["quantidade"] / total

            # 7️⃣ Exibe o gráfico de pizza com os profissionais ativos
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

            # 8️⃣ Exibe tabela detalhada
            st.dataframe(relatorio[["nome", "quantidade", "porcentagem"]])

        except Exception as e:
            st.error(f"Erro ao gerar relatório: {e}")
