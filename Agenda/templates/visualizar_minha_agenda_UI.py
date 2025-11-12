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
    def main(profissional_identifier):
        st.title("Minha Agenda")

        if not ARQUIVO_HORARIOS.exists():
            st.warning("Nenhum horário encontrado. Abra sua agenda primeiro.")
            return

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

        # --- Normaliza colunas ---
        df.columns = [c.lower().strip() for c in df.columns]

        # Renomeia colunas para padronizar
        if "id_profissional" in df.columns:
            df = df.rename(columns={"id_profissional": "profissional_id"})
        if "id_cliente" in df.columns:
            df = df.rename(columns={"id_cliente": "cliente"})
        if "id_servico" in df.columns:
            df = df.rename(columns={"id_servico": "serviço"})
        if "profissional_nome" not in df.columns:
            df["profissional_nome"] = ""

        # --- Preenche profissional_nome a partir do ID ---
        if "profissional_id" in df.columns:
            for i, row in df.iterrows():
                if row["profissional_id"]:  # se tem ID válido
                    p = ProfissionalDAO.listar_id(row["profissional_id"])
                    if p:
                        df.at[i, "profissional_nome"] = p.get_nome()

        # --- Filtra pelo profissional ---
        if isinstance(profissional_identifier, int):
            df_prof = df[df["profissional_id"] == profissional_identifier] if "profissional_id" in df.columns else pd.DataFrame()
        else:
            nome = str(profissional_identifier).strip().lower()
            df_prof = df[df["profissional_nome"].str.strip().str.lower() == nome]

        if df_prof.empty:
            st.info("Nenhum horário cadastrado para este profissional.")
            return

        # --- Conversores para nomes ---
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

        df_prof["Cliente"] = df_prof["cliente"].apply(get_nome_cliente) if "cliente" in df_prof.columns else "-"
        df_prof["Serviço"] = df_prof["serviço"].apply(get_nome_servico) if "serviço" in df_prof.columns else "-"
        df_prof["Profissional"] = df_prof["profissional_nome"].apply(lambda x: x.title() if x.strip() else "-")
        df_prof["Confirmado"] = df_prof["confirmado"].apply(lambda x: "Sim" if x else "Não") if "confirmado" in df_prof.columns else "-"

        # --- Monta DataFrame final ---
        if "data" in df_prof.columns:
            df_view = df_prof[["data", "Cliente", "Serviço", "Confirmado"]].copy()
            df_view = df_view.rename(columns={"data": "Data e Hora"})
        else:
            df_view = df_prof[["Cliente", "Serviço", "Confirmado", "Profissional"]].copy()

        st.dataframe(df_view, use_container_width=True)
