import streamlit as st
import pandas as pd
from views import View
from datetime import datetime
import time

class ManterHorarioUI:
    def main():
        st.header("Cadastro de Horários")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterHorarioUI.listar()
        with tab2: ManterHorarioUI.inserir()
        with tab3: ManterHorarioUI.atualizar()
        with tab4: ManterHorarioUI.excluir()

    def listar():
        horarios = View.horario_listar()
        if not horarios:
            st.write("Nenhum horário cadastrado")
        else:
            dic = []
            for obj in horarios:
                cliente = View.cliente_listar_id(obj.get_id_cliente())
                servico = View.servico_listar_id(obj.get_id_servico())
                profissional = View.profissional_listar_id(obj.get_id_profissional())
                dic.append({
                    "id": obj.get_id(),
                    "data": obj.get_data(),
                    "confirmado": obj.get_confirmado(),
                    "cliente": cliente.get_nome() if cliente else "",
                    "servico": servico.get_descricao() if servico else "",
                    "profissional": profissional.get_nome() if profissional else ""
                })
            st.dataframe(pd.DataFrame(dic))

    def inserir():
        clientes = View.cliente_listar()
        servicos = View.servico_listar()
        profissionais = View.profissional_listar()

        data = st.text_input("Informe a data e horário do serviço", datetime.now().strftime("%d/%m/%Y %H:%M"), key="inserir_data")
        confirmado = st.checkbox("Confirmado", key="inserir_confirmado")
        cliente = st.selectbox("Informe o cliente", clientes, key="inserir_cliente")
        servico = st.selectbox("Informe o serviço", servicos, key="inserir_servico")
        profissional = st.selectbox("Informe o profissional", profissionais, key="inserir_profissional")

        if st.button("Inserir", key="inserir_btn"):
            View.horario_inserir(
                datetime.strptime(data, "%d/%m/%Y %H:%M"),
                confirmado,
                cliente.get_id() if cliente else None,
                servico.get_id() if servico else None,
                profissional.get_id() if profissional else None
            )
            st.success("Horário inserido com sucesso")
            time.sleep(2)
            st.rerun()

    def atualizar():
        horarios = View.horario_listar()
        if not horarios:
            st.write("Nenhum horário cadastrado")
            return

        clientes = View.cliente_listar()
        servicos = View.servico_listar()
        profissionais = View.profissional_listar()

        op = st.selectbox("Atualização de Horários", horarios, key="atualizar_horario")
        data = st.text_input("Informe a nova data e horário", op.get_data().strftime("%d/%m/%Y %H:%M"), key=f"data_{op.get_id()}")
        confirmado = st.checkbox("Confirmado", value=op.get_confirmado(), key=f"confirmado_{op.get_id()}")

        cliente = st.selectbox(
            "Novo cliente",
            clientes,
            index=next((i for i, c in enumerate(clientes) if c.get_id() == op.get_id_cliente()), 0),
            key=f"cliente_{op.get_id()}"
        )
        servico = st.selectbox(
            "Novo serviço",
            servicos,
            index=next((i for i, s in enumerate(servicos) if s.get_id() == op.get_id_servico()), 0),
            key=f"servico_{op.get_id()}"
        )
        profissional = st.selectbox(
            "Novo profissional",
            profissionais,
            index=next((i for i, p in enumerate(profissionais) if p.get_id() == op.get_id_profissional()), 0),
            key=f"profissional_{op.get_id()}"
        )

        if st.button("Atualizar", key=f"atualizar_btn_{op.get_id()}"):
            View.horario_atualizar(
                op.get_id(),
                datetime.strptime(data, "%d/%m/%Y %H:%M"),
                confirmado,
                cliente.get_id() if cliente else None,
                servico.get_id() if servico else None,
                profissional.get_id() if profissional else None
            )
            st.success("Horário atualizado com sucesso")
            time.sleep(2)
            st.rerun()

    def excluir():
        horarios = View.horario_listar()
        if not horarios:
            st.write("Nenhum horário cadastrado")
            return

        op = st.selectbox("Exclusão de Horários", horarios, key="excluir_horario")
        if st.button("Excluir", key=f"excluir_btn_{op.get_id()}"):
            View.horario_excluir(op.get_id())
            st.success("Horário excluído com sucesso")
            time.sleep(2)
            st.rerun()
