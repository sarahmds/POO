import streamlit as st
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
from models.cliente import ClienteDAO
from models.servico import ServicoDAO
from models.profissional import ProfissionalDAO

BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_HORARIOS = BASE_DIR / "horarios.json"


def carregar_json(caminho):
    """Carrega JSON de horários e retorna DataFrame."""
    if not caminho.exists():
        # Cria DataFrame vazio com colunas esperadas
        return pd.DataFrame(columns=['id', 'data', 'confirmado', 'cliente', 'serviço', 'profissional_id', 'profissional_nome'])
    with open(caminho, "r", encoding="utf-8") as f:
        return pd.DataFrame(json.load(f))


def salvar_json(caminho, df):
    """Salva DataFrame em JSON."""
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, indent=4, ensure_ascii=False)


class ConfirmarServicoUI:

    @staticmethod
    def main(profissional_id: int):
        """Interface para o profissional confirmar serviços agendados."""

        st.title("Confirmar Serviço")

        agenda = carregar_json(ARQUIVO_HORARIOS)

        if agenda.empty:
            st.warning("Nenhum horário encontrado. Abra sua agenda primeiro.")
            return

        # --- Normaliza colunas e nomes ---
        agenda.columns = [c.lower().strip() for c in agenda.columns]
        if 'profissional_nome' in agenda.columns:
            agenda['profissional_nome'] = agenda['profissional_nome'].fillna("").str.strip().str.lower()

        # --- Obtém nome do profissional pelo ID, se existir ---
        if 'profissional_id' in agenda.columns:
            p = ProfissionalDAO.listar_id(profissional_id)
            nome_prof = p.get_nome().strip().lower() if p else ""
        else:
            nome_prof = ""

        # --- Filtra horários do profissional logado ---
        if 'profissional_id' in agenda.columns and agenda['profissional_id'].notna().any():
            # Usa ID quando disponível
            df_profissional = agenda[
                (agenda['profissional_id'] == profissional_id) &
                (agenda['cliente'].notna())
            ].copy()
        else:
            # Caso ID não exista ou seja nulo, filtra pelo nome
            df_profissional = agenda[
                (agenda['profissional_nome'] == nome_prof) &
                (agenda['cliente'].notna())
            ].copy()

        if df_profissional.empty:
            st.info("Nenhum serviço agendado por clientes para confirmar.")
            return

        # --- Converte coluna "data" para datetime ---
        df_profissional["data"] = pd.to_datetime(df_profissional["data"], format="%d/%m/%Y %H:%M", errors="coerce")
        df_profissional = df_profissional.dropna(subset=["data"])

        # --- Funções para converter IDs em nomes ---
        def get_nome_cliente(id_cliente):
            if not id_cliente:
                return "-"
            try:
                c = ClienteDAO.listar_id(int(id_cliente))
                return c.get_nome() if c else str(id_cliente)
            except:
                return str(id_cliente)

        def get_nome_servico(id_servico):
            if not id_servico:
                return "-"
            try:
                s = ServicoDAO.listar_id(int(id_servico))
                return s.get_descricao() if s else str(id_servico)
            except:
                return str(id_servico)

        # --- Lista de horários para o selectbox ---
        opcoes_horarios = [
            f"{int(row['id'])} - {row['data'].strftime('%d/%m/%Y %H:%M')} - {get_nome_cliente(row['cliente'])} - {get_nome_servico(row['serviço'])} - {'Confirmado' if row['confirmado'] else 'Pendente'}"
            for _, row in df_profissional.iterrows()
        ]

        horario_escolhido = st.selectbox("Selecione o horário agendado:", opcoes_horarios)
        horario_id = int(horario_escolhido.split(" - ")[0])

        # --- Botão de confirmação ---
        if st.button("Confirmar"):
            idx = agenda[agenda["id"] == horario_id].index
            if not idx.empty:
                agenda.at[idx[0], "confirmado"] = True
                salvar_json(ARQUIVO_HORARIOS, agenda)
                st.success("Serviço confirmado!")

            # --- Mostra resumo atualizado ---
            if 'profissional_id' in agenda.columns and agenda['profissional_id'].notna().any():
                df_atualizado = agenda[agenda['profissional_id'] == profissional_id].copy()
            else:
                df_atualizado = agenda[agenda['profissional_nome'] == nome_prof].copy()

            df_atualizado["data"] = pd.to_datetime(df_atualizado["data"], format="%d/%m/%Y %H:%M", errors="coerce")
            df_atualizado["cliente"] = df_atualizado["cliente"].apply(get_nome_cliente)
            df_atualizado["serviço"] = df_atualizado["serviço"].apply(get_nome_servico)
            df_atualizado["confirmado"] = df_atualizado["confirmado"].apply(lambda x: "Sim" if x else "Não")

            st.subheader("Horários Atualizados")
            st.dataframe(
                df_atualizado[["id", "data", "cliente", "serviço", "confirmado"]],
                use_container_width=True
            )
