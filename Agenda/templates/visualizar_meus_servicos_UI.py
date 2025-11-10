import streamlit as st
import pandas as pd
import json
from pathlib import Path
from models.profissional import ProfissionalDAO
from models.servico import ServicoDAO

BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_HORARIOS = BASE_DIR / "horarios.json"

class VisualizarMeusServicosUI:

    @staticmethod
    def main(cliente_id: int):
        """Interface para o cliente visualizar seus serviços agendados."""

        st.title("Meus Serviços")

        try:
            if not ARQUIVO_HORARIOS.exists():
                st.warning("Nenhum serviço encontrado. Nenhum horário foi agendado ainda.")
                return

            # Carrega o arquivo JSON
            with open(ARQUIVO_HORARIOS, "r", encoding="utf-8") as f:
                agenda_data = json.load(f)

            if not agenda_data:
                st.info("Nenhum serviço encontrado.")
                return

            df = pd.DataFrame(agenda_data)
            if df.empty:
                st.info("Nenhum serviço encontrado.")
                return

            # Garante que a coluna de cliente exista
            if "id_cliente" not in df.columns:
                st.error("Coluna 'id_cliente' não encontrada no arquivo de horários.")
                return

            # Filtra apenas os serviços do cliente logado
            df_cliente = df[df["id_cliente"] == cliente_id].copy()

            if df_cliente.empty:
                st.info("Você ainda não possui serviços agendados.")
                return

            # Converter IDs em nomes legíveis
            def get_nome_profissional(id_):
                try:
                    p = ProfissionalDAO.listar_id(int(id_))
                    return p.get_nome() if p else f"Profissional {id_}"
                except:
                    return f"Profissional {id_}"

            def get_nome_servico(id_):
                try:
                    s = ServicoDAO.listar_id(int(id_))
                    return s.get_descricao() if s else f"Serviço {id_}"
                except:
                    return f"Serviço {id_}"

            # Cria colunas legíveis
            df_cliente["Profissional"] = df_cliente["id_profissional"].apply(get_nome_profissional)
            df_cliente["Serviço"] = df_cliente["id_servico"].apply(get_nome_servico)
            df_cliente["Confirmado"] = df_cliente["confirmado"].apply(lambda x: "Sim" if x else "Não")

            # Seleciona colunas relevantes
            df_view = df_cliente[["id", "data", "Serviço", "Profissional", "Confirmado"]].copy()
            df_view = df_view.rename(columns={"id": "ID", "data": "Data e Hora"})

            # Exibe tabela
            st.data_editor(
                df_view,
                hide_index=True,
                disabled=True,
                use_container_width=True,
            )

        except Exception as e:
            st.error(f"Erro ao carregar serviços: {e}")
