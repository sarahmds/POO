import streamlit as st
import pandas as pd
import json
from pathlib import Path
from views import View
from models.profissional import ProfissionalDAO

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


class AgendarServicoUI:

    @staticmethod
    def main(cliente_id: int):
        st.title("Agendar Serviço")

        DATA_DIR.mkdir(exist_ok=True)
        agenda = carregar_json(HORARIOS_FILE)

        if agenda.empty:
            st.warning("Nenhum horário disponível para agendamento.")
            return

        # Filtra horários sem cliente (disponíveis)
        df_disponivel = agenda[agenda['cliente'].isnull()].copy()

        if df_disponivel.empty:
            st.info("Nenhum horário disponível no momento.")
            return

        def formatar_horario(idx):
            linha = df_disponivel.loc[idx]
            prof_id = linha['profissional']
            try:
                prof = ProfissionalDAO.listar_id(int(prof_id))
                prof_nome = prof.get_nome() if prof else f"ID {prof_id}"
            except Exception:
                prof_nome = f"ID {prof_id}"
            return f"{linha['data']} com Profissional {prof_nome}"

        df_disponivel.reset_index(drop=True, inplace=True)
        opcao = st.selectbox(
            "Selecione um horário disponível:",
            options=df_disponivel.index,
            format_func=formatar_horario
        )

        servicos = View.servico_listar()
        if not servicos:
            st.error("Nenhum serviço cadastrado.")
            return

        servico_opcao = st.selectbox(
            "Selecione o serviço desejado:",
            options=servicos,
            format_func=lambda s: s.get_descricao()
        )

        if st.button("Confirmar Agendamento"):
            idx_global = df_disponivel.loc[opcao, 'id']
            agenda.loc[agenda['id'] == idx_global, 'cliente'] = cliente_id
            agenda.loc[agenda['id'] == idx_global, 'serviço'] = servico_opcao.get_descricao()
            agenda.loc[agenda['id'] == idx_global, 'confirmado'] = False

            salvar_json(HORARIOS_FILE, agenda)
