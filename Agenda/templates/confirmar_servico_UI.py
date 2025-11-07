import streamlit as st
import pandas as pd
import json
from pathlib import Path

DATA_DIR = Path("data")
HORARIOS_FILE = DATA_DIR / "horarios.json"

def carregar_json(caminho):
    if not caminho.exists():
        return pd.DataFrame(columns=['id', 'data', 'confirmado', 'cliente', 'serviço', 'profissional'])
    with open(caminho, "r", encoding="utf-8") as f:
        return pd.DataFrame(json.load(f))

def salvar_json(caminho, df):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, indent=4, ensure_ascii=False)


class ConfirmarServicoUI:

    @staticmethod
    def main(profissional_id: int):
        """Interface para o profissional confirmar serviços agendados."""

        st.title("Confirmar Serviço")

        DATA_DIR.mkdir(exist_ok=True)
        agenda = carregar_json(HORARIOS_FILE)

        if agenda.empty:
            st.warning("Nenhum horário encontrado. Abra sua agenda primeiro.")
            return

        # Filtra horários com cliente marcado para o profissional logado
        df_profissional = agenda[
            (agenda['profissional'].astype(str) == str(profissional_id)) &
            (agenda['cliente'].notna())
        ].copy()

        if df_profissional.empty:
            st.info("Nenhum serviço agendado por clientes para confirmar.")
            return

        # Corrige data que está como string
        def formatar_data(valor):
            try:
                return datetime.strptime(valor, "%d/%m/%Y %H:%M")
            except Exception:
                return valor

        if df_profissional["data"].dtype == object:
            df_profissional["data"] = df_profissional["data"].apply(formatar_data)

        opcoes_horarios = [
            f"{int(row['id'])} - {row['data'].strftime('%d/%m/%Y %H:%M')} - {'Confirmado' if row['confirmado'] else 'Pendente'}"
            for _, row in df_profissional.iterrows()
        ]

        horario_escolhido = st.selectbox("Selecione o horário agendado:", opcoes_horarios)
        horario_id = int(horario_escolhido.split(" - ")[0])

        # Lista de clientes já agendados
        clientes = df_profissional['cliente'].dropna().unique()
        if len(clientes) > 0:
            cliente_opcoes = [str(c) for c in clientes]
            cliente_selecionado = st.selectbox("Cliente", cliente_opcoes)
        else:
            st.info("Nenhum cliente agendado.")
            return

        if st.button("Confirmar"):
            idx = agenda[agenda["id"] == horario_id].index
            if not idx.empty:
                agenda.at[idx[0], "confirmado"] = True
                salvar_json(HORARIOS_FILE, agenda)
                st.success("Serviço confirmado com sucesso!")

            # Mostra resumo atualizado
            df_atualizado = agenda[
                agenda["profissional"].astype(str) == str(profissional_id)
            ][["id", "data", "confirmado", "cliente", "serviço"]]
            st.dataframe(df_atualizado, use_container_width=True)
