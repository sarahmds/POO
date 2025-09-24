import streamlit as st
import pandas as pd
from views import View
import time
from datetime import datetime

class ManterHorarioUI:

    @staticmethod
    def main():
        st.header("Cadastro de Horários")

        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])

        with tab1:
            ManterHorarioUI.listar()
        with tab2:
            ManterHorarioUI.inserir()
        with tab3:
            ManterHorarioUI.atualizar()
        with tab4:
            ManterHorarioUI.excluir()

    @staticmethod
    def listar():
        horarios = View.horario_listar()

        if len(horarios) == 0:
            st.write("Nenhum horário cadastrado")
        else:
            dic = []
            for obj in horarios:
                cliente = View.cliente_listar_id(obj.get_id_cliente())
                servico = View.servico_listar_id(obj.get_id_servico())

                nome_cliente = cliente.get_nome() if cliente is not None else "Desconhecido"
                descricao_servico = servico.get_descricao() if servico is not None else "Desconhecido"

                dic.append({
                    "id": obj.get_id(),
                    "data": obj.get_data(),
                    "confirmado": obj.get_confirmado(),
                    "cliente": nome_cliente,
                    "serviço": descricao_servico
                })

            df = pd.DataFrame(dic)
            st.dataframe(df)

    @staticmethod
    def inserir():
        clientes = View.cliente_listar()
        servicos = View.servico_listar()

        data = st.text_input(
            "Informe a data e horário do serviço",
            datetime.now().strftime("%d/%m/%Y %H:%M")
        )
        confirmado = st.checkbox("Confirmado")

        cliente = st.selectbox("Informe o cliente", clientes, format_func=lambda c: c.get_nome())
        servico = st.selectbox("Informe o serviço", servicos, format_func=lambda s: s.get_descricao())

        if st.button("Inserir"):
            id_cliente = cliente.get_id() if cliente is not None else None
            id_servico = servico.get_id() if servico is not None else None

            try:
                data_dt = datetime.strptime(data, "%d/%m/%Y %H:%M")
                View.horario_inserir(data_dt, confirmado, id_cliente, id_servico)
                st.success("Horário inserido com sucesso")
            except ValueError:
                st.error("Formato de data/hora inválido. Use dd/mm/aaaa HH:MM.")

    @staticmethod
    def atualizar():
        horarios = View.horario_listar()

        if len(horarios) == 0:
            st.write("Nenhum horário cadastrado")
            return

        clientes = View.cliente_listar()
        servicos = View.servico_listar()

        op = st.selectbox("Atualização de Horários", horarios, format_func=lambda h: f"{h.get_id()} - {h.get_data()}")

        data = st.text_input("Informe a nova data e horário do serviço", op.get_data().strftime("%d/%m/%Y %H:%M"))
        confirmado = st.checkbox("Nova confirmação", value=op.get_confirmado())

        id_cliente = op.get_id_cliente()
        id_servico = op.get_id_servico()

        cliente = st.selectbox(
            "Informe o novo cliente",
            clientes,
            index=next((i for i, c in enumerate(clientes) if c.get_id() == id_cliente), 0),
            format_func=lambda c: c.get_nome()
        )
        servico = st.selectbox(
            "Informe o novo serviço",
            servicos,
            index=next((i for i, s in enumerate(servicos) if s.get_id() == id_servico), 0),
            format_func=lambda s: s.get_descricao()
        )

        if st.button("Atualizar"):
            id_cliente = cliente.get_id() if cliente is not None else None
            id_servico = servico.get_id() if servico is not None else None

            try:
                data_dt = datetime.strptime(data, "%d/%m/%Y %H:%M")
                View.horario_atualizar(op.get_id(), data_dt, confirmado, id_cliente, id_servico)
                st.success("Horário atualizado com sucesso")
            except ValueError:
                st.error("Formato de data/hora inválido. Use dd/mm/aaaa HH:MM.")

    @staticmethod
    def excluir():
        horarios = View.horario_listar()

        if len(horarios) == 0:
            st.write("Nenhum horário cadastrado")
            return

        op = st.selectbox("Exclusão de Horários", horarios, format_func=lambda h: f"{h.get_id()} - {h.get_data()}")

        if st.button("Excluir"):
            View.horario_excluir(op.get_id())
            st.success("Horário excluído com sucesso")
            time.sleep(2)
            st.experimental_rerun()
