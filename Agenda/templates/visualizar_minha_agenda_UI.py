import streamlit as st
import pandas as pd
from views import View

class VisualizarMinhaAgendaUI:

    @staticmethod
    def main(profissional_identifier):
        st.title("Minha Agenda")

        try:
            # ✅ Lê todos os horários via View (sem acessar JSON diretamente)
            horarios = View.horario_listar()
            if not horarios:
                st.info("Nenhum horário cadastrado ainda.")
                return

            df = pd.DataFrame([h.to_json() for h in horarios])
            if df.empty:
                st.info("Nenhum horário cadastrado ainda.")
                return

            # --- Normaliza colunas ---
            df.columns = [c.lower().strip() for c in df.columns]
            df.rename(columns={
                "id_profissional": "profissional_id",
                "id_cliente": "cliente",
                "id_servico": "servico"
            }, inplace=True)

            # --- Completa dados do profissional ---
            df["profissional_nome"] = df["profissional_id"].apply(
                lambda pid: View.profissional_listar_id(pid).get_nome()
                if pid and View.profissional_listar_id(pid) else "-"
            )

            # --- Filtra pelo profissional (por ID ou nome) ---
            df_prof = pd.DataFrame()
            if isinstance(profissional_identifier, int):
                df_prof = df[df["profissional_id"] == profissional_identifier]
            if df_prof.empty and isinstance(profissional_identifier, str):
                nome = profissional_identifier.strip().lower()
                df_prof = df[df["profissional_nome"].str.strip().str.lower() == nome]

            if df_prof.empty:
                st.info("Nenhum horário cadastrado para este profissional.")
                return

            # --- Conversores para nomes ---
            def get_nome_cliente(val):
                try:
                    c = View.cliente_listar_id(int(val))
                    return c.get_nome() if c else f"Cliente {val}"
                except:
                    return f"Cliente {val}"

            def get_nome_servico(val):
                try:
                    s = View.servico_listar_id(int(val))
                    return s.get_descricao() if s else f"Serviço {val}"
                except:
                    return f"Serviço {val}"

            # Cria colunas legíveis
            df_prof["Cliente"] = df_prof["cliente"].apply(get_nome_cliente)
            df_prof["Serviço"] = df_prof["servico"].apply(get_nome_servico)
            df_prof["Profissional"] = df_prof["profissional_nome"].apply(
                lambda x: x.title() if isinstance(x, str) and x.strip() else "-"
            )
            df_prof["Confirmado"] = df_prof["confirmado"].apply(
                lambda x: "Sim" if str(x).strip().lower() in ["true", "1", "sim"] else "Não"
            ) if "confirmado" in df_prof.columns else "-"

            # --- Monta DataFrame final ---
            colunas = ["data", "Cliente", "Serviço", "Confirmado"]
            colunas = [c for c in colunas if c in df_prof.columns]
            df_view = df_prof[colunas].copy()
            if "data" in df_view.columns:
                df_view.rename(columns={"data": "Data e Hora"}, inplace=True)

            st.data_editor(
                df_view,
                hide_index=True,
                disabled=True,
                use_container_width=True,
            )

        except Exception as e:
            st.error(f"Erro ao carregar agenda: {e}")
