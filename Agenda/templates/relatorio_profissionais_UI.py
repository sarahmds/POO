import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from views import View

class RelatorioProfissionaisUI:

    @staticmethod
    def main():

        profissionais = View.profissional_listar()
        if not profissionais:
            st.warning("Não há profissionais cadastrados.")
            return

        df_profissionais = pd.DataFrame([{
            'id': p.get_id(),
            'nome': p.get_nome()
        } for p in profissionais])

        if 'agenda' not in st.session_state or st.session_state.agenda.empty:
            st.warning("Nenhum serviço agendado ainda.")
            return

        df_agenda = st.session_state.agenda.copy()
        df_agenda['confirmado'] = df_agenda['confirmado'].fillna(False)

        relatorio = df_agenda[df_agenda['confirmado'] == True].groupby('profissional').size().reset_index(name='quantidade')

        relatorio = df_profissionais.merge(relatorio, how='left', left_on='id', right_on='profissional')
        relatorio['quantidade'] = relatorio['quantidade'].fillna(0)

        total = relatorio['quantidade'].sum()
        if total == 0:
            st.info("Nenhum serviço confirmado para gerar o relatório.")
            return

        relatorio['porcentagem'] = 100 * relatorio['quantidade'] / total

        fig, ax = plt.subplots()
        ax.pie(relatorio['quantidade'], labels=relatorio['nome'], autopct='%1.1f%%')
        ax.set_title("Porcentagem de Serviços Confirmados por Profissional")
        st.pyplot(fig)

        st.dataframe(relatorio[['nome', 'quantidade', 'porcentagem']])
