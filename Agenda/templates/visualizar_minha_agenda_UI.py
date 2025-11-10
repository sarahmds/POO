import streamlit as st
import pandas as pd
import json
from pathlib import Path
from models.cliente import ClienteDAO
from models.servico import ServicoDAO
from models.profissional import ProfissionalDAO

BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_HORARIOS = BASE_DIR / "horarios.json"

class VisualizarMinhaAgendaUI:

    @staticmethod
    def main(profissional_id: int):
        st.title("Minha Agenda")

        if not ARQUIVO_HORARIOS.exists():
            st.warning("Nenhum horário encontrado. Abra sua agenda primeiro.")
            return

        # Carrega JSON
        try:
            with open(ARQUIVO_HORARIOS, "r", encoding="utf-8") as f:
                agenda_data = json.load(f)
        except Exception as e:
            st.error(f"Erro ao ler arquivo de agenda: {e}")
            return

        if not agenda_data:
            st.info("Nenhum horário cadastrado ainda.")
            return

        df = pd.DataFrame(agenda_data)
        if df.empty:
            st.info("Nenhum horário cadastrado ainda.")
            return

        # Normaliza nomes de colunas
        df.rename(columns={
            "id_cliente": "cliente",
            "id_servico": "serviço",
            "id_profissional": "profissional"
        }, inplace=True)

        # Confirma que as colunas essenciais existem
        if "profissional" not in df.columns:
            st.error("Coluna do profissional não encontrada na agenda.")
            return

        # Filtra pelo profissional logado
        df_prof = df[df["profissional"] == profissional_id].copy()
        if df_prof.empty:
            st.info("Nenhum horário cadastrado para este profissional.")
            return

        # Funções para converter IDs em nomes
        def get_nome_cliente(val):
            if not val or pd.isna(val):
                return "-"
            try:
                c = ClienteDAO.listar_id(int(val))
                return c.get_nome() if c else str(val)
            except:
                return str(val)

        def get_nome_servico(val):
            if not val or pd.isna(val):
                return "-"
            try:
                s = ServicoDAO.listar_id(int(val))
                return s.get_descricao() if s else str(val)
            except:
                return str(val)

        def get_nome_profissional(val):
            if not val or pd.isna(val):
                return "-"
            try:
                p = ProfissionalDAO.listar_id(int(val))
                return p.get_nome() if p else str(val)
            except:
                return str(val)

        # Aplica conversões
        df_prof["Cliente"] = df_prof["cliente"].apply(get_nome_cliente)
        df_prof["Serviço"] = df_prof["serviço"].apply(get_nome_servico)
        df_prof["Profissional"] = df_prof["profissional"].apply(get_nome_profissional)
        df_prof["Confirmado"] = df_prof["confirmado"].apply(lambda x: "Sim" if x else "Não")

        # Seleciona colunas para exibir
        df_view = df_prof[["data", "Cliente", "Serviço", "Confirmado"]].copy()
        df_view = df_view.rename(columns={"data": "Data e Hora"})

        st.dataframe(df_view, use_container_width=True)
