import streamlit as st
import pandas as pd
from views import View

class VisualizarMeusServicosUI:

    @staticmethod
    def main(cliente_id: int):
        """Interface para o cliente visualizar seus serviços agendados."""
        st.title("Meus Serviços")

        try:
            # ✅ Lê os horários através da View (sem acessar o JSON diretamente)
            horarios = View.horario_listar()
            if not horarios:
                st.info("Nenhum serviço encontrado.")
                return

            # Converte objetos em dicionários
            df = pd.DataFrame([h.to_json() for h in horarios])
            if df.empty:
                st.info("Nenhum serviço encontrado.")
                return

            # Verifica se existe a coluna 'id_cliente'
            if "id_cliente" not in df.columns:
                st.error("Coluna 'id_cliente' não encontrada nos dados de horários.")
                return

            # Filtra apenas os serviços do cliente logado
            df_cliente = df[df["id_cliente"] == cliente_id].copy()
            if df_cliente.empty:
                st.info("Você ainda não possui serviços agendados.")
                return

            # ✅ Obtém nomes de profissional e serviço via View
            def get_nome_profissional(id_):
                try:
                    p = View.profissional_listar_id(int(id_))
                    return p.get_nome() if p else f"Profissional {id_}"
                except:
                    return f"Profissional {id_}"

            def get_nome_servico(id_):
                try:
                    s = View.servico_listar_id(int(id_))
                    return s.get_descricao() if s else f"Serviço {id_}"
                except:
                    return f"Serviço {id_}"

            # Cria colunas legíveis
            df_cliente["Profissional"] = df_cliente["id_profissional"].apply(get_nome_profissional)
            df_cliente["Serviço"] = df_cliente["id_servico"].apply(get_nome_servico)

            # Corrige valores booleanos de confirmado
            if "confirmado" in df_cliente.columns:
                df_cliente["Confirmado"] = df_cliente["confirmado"].apply(lambda x: "Sim" if str(x).lower() in ["true", "1", "sim"] else "Não")
            else:
                df_cliente["Confirmado"] = "Não informado"

            # Seleciona e renomeia colunas relevantes
            colunas_validas = [c for c in ["id", "data", "Serviço", "Profissional", "Confirmado"] if c in df_cliente.columns]
            df_view = df_cliente[colunas_validas].copy()
            df_view.rename(columns={"id": "ID", "data": "Data e Hora"}, inplace=True)

            # Exibe tabela com os serviços
            st.data_editor(
                df_view,
                hide_index=True,
                disabled=True,
                use_container_width=True,
            )

        except Exception as e:
            st.error(f"Erro ao carregar serviços: {e}")
