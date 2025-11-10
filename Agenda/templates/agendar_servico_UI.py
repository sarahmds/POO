import streamlit as st
import pandas as pd
import json
from pathlib import Path
from views import View
from models.profissional import ProfissionalDAO

BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_HORARIOS = BASE_DIR / "horarios.json"


def carregar_json(caminho):
    """Carrega os horários do arquivo JSON e converte em DataFrame."""
    if not caminho.exists():
        return pd.DataFrame(columns=['id', 'data', 'confirmado', 'id_cliente', 'id_servico', 'id_profissional'])
    with open(caminho, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return pd.DataFrame(data)
        except json.JSONDecodeError:
            return pd.DataFrame(columns=['id', 'data', 'confirmado', 'id_cliente', 'id_servico', 'id_profissional'])


def salvar_json(caminho, df):
    """Salva o DataFrame no arquivo JSON."""
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, indent=4, ensure_ascii=False)


class AgendarServicoUI:

    @staticmethod
    def main(cliente_id: int):
        st.title("Agendar Serviço")

        agenda = carregar_json(ARQUIVO_HORARIOS)

        if agenda.empty:
            st.warning("Nenhum horário disponível para agendamento.")
            return

        # Filtra horários que ainda não têm cliente
        df_disponivel = agenda[agenda['id_cliente'].isnull()].copy()

        if df_disponivel.empty:
            st.info("Nenhum horário disponível no momento.")
            return

        # Função para exibir o nome do profissional
        def formatar_horario(idx):
            linha = df_disponivel.loc[idx]
            prof_id = linha['id_profissional']
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

        # Lista de serviços disponíveis
        servicos = View.servico_listar()
        if not servicos:
            st.error("Nenhum serviço cadastrado.")
            return

        servico_opcao = st.selectbox(
            "Selecione o serviço desejado:",
            options=servicos,
            format_func=lambda s: s.get_descricao()
        )

        # Confirmar agendamento
        if st.button("Confirmar Agendamento"):
            idx_global = df_disponivel.loc[opcao, 'id']

            agenda.loc[agenda['id'] == idx_global, 'id_cliente'] = cliente_id
            agenda.loc[agenda['id'] == idx_global, 'id_servico'] = servico_opcao.get_id()
            agenda.loc[agenda['id'] == idx_global, 'confirmado'] = False

            salvar_json(ARQUIVO_HORARIOS, agenda)
            st.success("Serviço agendado com sucesso!")
