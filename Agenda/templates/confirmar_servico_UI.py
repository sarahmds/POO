import streamlit as st
import pandas as pd
from datetime import datetime
from views import View
from models.cliente import ClienteDAO
from models.servico import ServicoDAO
from models.profissional import ProfissionalDAO

class ConfirmarServicoUI:

    @staticmethod
    def main(profissional_id: int):
        """Interface para o profissional confirmar serviços agendados."""

        st.title("Confirmar Serviço")

        # --- Lê horários via View ---
        agenda = View.horario_listar()

        if not agenda:
            st.warning("Nenhum horário encontrado. Abra sua agenda primeiro.")
            return

        # --- Filtra horários do profissional logado que tenham cliente e não confirmados ---
        horarios_filtrados = [
            h for h in agenda
            if h.get_id_profissional() == profissional_id and h.get_id_cliente() and not h.get_confirmado()
        ]

        if not horarios_filtrados:
            st.info("Nenhum serviço pendente para confirmar.")
            return

        # --- Prepara dataframe para exibição ---
        df = pd.DataFrame([
            {
                "id": h.get_id(),
                "data": h.get_data().strftime("%d/%m/%Y %H:%M") if isinstance(h.get_data(), datetime) else str(h.get_data()),
                "id_cliente": h.get_id_cliente(),
                "id_servico": h.get_id_servico(),
                "confirmado": h.get_confirmado(),
                "profissional_nome": getattr(h, "profissional_nome", "—")
            }
            for h in horarios_filtrados
        ])

        # --- Conversores auxiliares ---
        def get_nome_cliente(id_cliente):
            if not id_cliente:
                return "-"
            c = ClienteDAO.listar_id(int(id_cliente))
            return c.get_nome() if c else str(id_cliente)

        def get_nome_servico(id_servico):
            if not id_servico:
                return "-"
            s = ServicoDAO.listar_id(int(id_servico))
            return s.get_descricao() if s else str(id_servico)

        # --- Opções para selectbox ---
        opcoes_horarios = [
            f"{row['id']} - {row['data']} - {get_nome_cliente(row['id_cliente'])} - {get_nome_servico(row['id_servico'])}"
            for _, row in df.iterrows()
        ]

        horario_escolhido = st.selectbox("Selecione o horário agendado:", opcoes_horarios)
        horario_id = int(horario_escolhido.split(" - ")[0])

        # --- Botão de confirmação ---
        if st.button("Confirmar"):
            try:
                # --- Só confirma se houver cliente ---
                h = next((h for h in horarios_filtrados if h.get_id() == horario_id), None)
                if not h or not h.get_id_cliente():
                    st.error("Não é possível confirmar um horário sem cliente.")
                    return

                # --- Confirma o horário ---
                View.horario_atualizar(
                    id=h.get_id(),
                    data=h.get_data(),
                    confirmado=True,
                    id_cliente=h.get_id_cliente(),
                    id_servico=h.get_id_servico(),
                    id_profissional=h.get_id_profissional()
                )
                st.success("Serviço confirmado com sucesso!")

                # --- Atualiza exibição ---
                df_atualizado = pd.DataFrame([
                    {
                        "id": h.get_id(),
                        "data": h.get_data().strftime("%d/%m/%Y %H:%M"),
                        "id_cliente": get_nome_cliente(h.get_id_cliente()),
                        "id_servico": get_nome_servico(h.get_id_servico()),
                        "confirmado": "Sim" if h.get_confirmado() else "Não",
                        "profissional_nome": getattr(h, "profissional_nome", "—")
                    }
                    for h in View.horario_listar()
                    if h.get_id_profissional() == profissional_id
                ])

                st.subheader("Horários Atualizados")
                st.dataframe(df_atualizado[["id", "data", "id_cliente", "id_servico", "confirmado"]], use_container_width=True)

            except Exception as e:
                st.error(f"Erro ao confirmar serviço: {e}")
