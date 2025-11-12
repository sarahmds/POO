import streamlit as st
import pandas as pd
from views import View
from datetime import datetime
import time
from templates.loginUI import carregar_usuario

class ManterHorarioUI:
    """CRUD de Horários (Admin, Profissional e Cliente)"""

    @staticmethod
    def main():
        try:
            tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
            with tab1:
                ManterHorarioUI.listar()
            with tab2:
                ManterHorarioUI.inserir()
            with tab3:
                ManterHorarioUI.atualizar()
            with tab4:
                ManterHorarioUI.excluir()
        except Exception as e:
            st.error(f"Erro ao carregar interface de horários: {e}")

    @staticmethod
    def listar():
        try:
            usuario = carregar_usuario()
            if not usuario:
                st.error("Usuário não autenticado.")
                return

            horarios = View.horario_listar()
            dados = []

            for obj in horarios:
                id_cliente = int(obj.get_id_cliente()) if obj.get_id_cliente() else None
                id_servico = int(obj.get_id_servico()) if obj.get_id_servico() else None
                id_profissional = int(obj.get_id_profissional()) if obj.get_id_profissional() else None

                # Buscar objetos no banco
                cliente_obj = View.cliente_listar_id(id_cliente) if id_cliente else None
                servico_obj = View.servico_listar_id(id_servico) if id_servico else None

                # FILTRO POR USUÁRIO
                if usuario["tipo"] == "cliente" and id_cliente != usuario["id"]:
                    continue
                if usuario["tipo"] == "profissional" and id_profissional != usuario["id"]:
                    continue

                dados.append({
                    "ID": obj.get_id(),
                    "Data": obj.get_data().strftime("%d/%m/%Y %H:%M"),
                    "Confirmado": "Sim" if obj.get_confirmado() else "Não",
                    "Cliente": cliente_obj.get_nome() if cliente_obj else "—",
                    "Serviço": servico_obj.get_descricao() if servico_obj else "—",
                    "Profissional": getattr(obj, "profissional_nome", "—")
                })

            if not dados:
                st.info("Nenhum horário encontrado para o seu usuário.")
                return

            df = pd.DataFrame(dados, columns=["ID", "Data", "Confirmado", "Cliente", "Serviço", "Profissional"])
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao listar horários: {e}")

    @staticmethod
    def inserir():
        try:
            clientes = View.cliente_listar()
            servicos = View.servico_listar()
            profissionais = View.profissional_listar()

            if not clientes or not servicos or not profissionais:
                st.warning("Cadastre Cliente, Serviço e Profissional antes de inserir um horário.")
                return

            data = st.text_input(
                "Data e horário (dd/mm/aaaa HH:MM)",
                datetime.now().strftime("%d/%m/%Y %H:%M"),
                key="inserir_data"
            )
            confirmado = st.checkbox("Confirmado", key="inserir_confirmado")
            cliente = st.selectbox("Cliente", clientes, key="inserir_cliente")
            servico = st.selectbox("Serviço", servicos, key="inserir_servico")
            profissional = st.selectbox("Profissional", profissionais, key="inserir_profissional")

            if st.button("Inserir", key="inserir_btn"):
                try:
                    data_obj = datetime.strptime(data, "%d/%m/%Y %H:%M")
                    View.horario_inserir(
                        data_obj,
                        confirmado,
                        cliente.get_id(),
                        servico.get_id(),
                        profissional.get_id()
                    )
                    st.success(
                        f"Horário inserido: {cliente.get_nome()} - {servico.get_descricao()} com {profissional.get_nome()}."
                    )
                    time.sleep(2)
                    st.rerun()
                except ValueError:
                    st.error("Formato de data e horário inválido.")
                except Exception as e:
                    st.error(f"Erro ao inserir horário: {e}")
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")

    @staticmethod
    def atualizar():
        try:
            usuario = carregar_usuario()
            if not usuario:
                st.error("Usuário não autenticado.")
                return

            if usuario["tipo"] == "cliente":
                st.warning("Clientes não podem atualizar horários pelo painel. Use sua área de cliente.")
                return

            horarios = View.horario_listar()
            if usuario["tipo"] == "profissional":
                horarios = [h for h in horarios if h.get_id_profissional() == usuario["id"]]

            if not horarios:
                st.info("Nenhum horário disponível para atualizar.")
                return

            clientes = View.cliente_listar()
            servicos = View.servico_listar()
            profissionais = View.profissional_listar()

            op = st.selectbox(
                "Selecione o horário para atualizar",
                horarios,
                format_func=lambda x: f"{x.get_data().strftime('%d/%m/%Y %H:%M')} - {x.get_id()}"
            )

            cliente_index = next((i for i, c in enumerate(clientes) if c.get_id() == op.get_id_cliente()), 0)
            servico_index = next((i for i, s in enumerate(servicos) if s.get_id() == op.get_id_servico()), 0)
            profissional_index = next((i for i, p in enumerate(profissionais) if p.get_id() == op.get_id_profissional()), 0)

            data = st.text_input(
                "Nova data e horário (dd/mm/aaaa HH:MM)",
                op.get_data().strftime("%d/%m/%Y %H:%M"),
                key=f"data_{op.get_id()}"
            )
            confirmado = st.checkbox("Confirmado", value=op.get_confirmado(), key=f"confirmado_{op.get_id()}")
            cliente = st.selectbox("Novo cliente", clientes, index=cliente_index, key=f"cliente_{op.get_id()}")
            servico = st.selectbox("Novo serviço", servicos, index=servico_index, key=f"servico_{op.get_id()}")
            profissional = st.selectbox("Novo profissional", profissionais, index=profissional_index, key=f"profissional_{op.get_id()}")

            if st.button("Atualizar", key=f"atualizar_btn_{op.get_id()}"):
                try:
                    data_obj = datetime.strptime(data, "%d/%m/%Y %H:%M")
                    View.horario_atualizar(
                        op.get_id(),
                        data_obj,
                        confirmado,
                        cliente.get_id(),
                        servico.get_id(),
                        profissional.get_id()
                    )
                    st.success("Horário atualizado com sucesso.")
                    time.sleep(2)
                    st.rerun()
                except ValueError:
                    st.error("Formato de data inválido.")
                except Exception as e:
                    st.error(f"Erro ao atualizar: {e}")
        except Exception as e:
            st.error(f"Erro ao carregar dados para atualização: {e}")

    @staticmethod
    def excluir():
        try:
            usuario = carregar_usuario()
            if not usuario:
                st.error("Usuário não autenticado.")
                return

            horarios = View.horario_listar()
            if usuario["tipo"] == "profissional":
                horarios = [h for h in horarios if h.get_id_profissional() == usuario["id"]]
            if usuario["tipo"] == "cliente":
                horarios = [h for h in horarios if h.get_id_cliente() == usuario["id"]]

            if not horarios:
                st.info("Nenhum horário cadastrado.")
                return

            op = st.selectbox(
                "Selecione o horário para excluir",
                horarios,
                format_func=lambda x: f"{x.get_data().strftime('%d/%m/%Y %H:%M')} - {x.get_id()}"
            )
            if st.button("Excluir", key=f"excluir_btn_{op.get_id()}"):
                try:
                    cliente = View.cliente_listar_id(op.get_id_cliente()) if op.get_id_cliente() else None
                    servico = View.servico_listar_id(op.get_id_servico()) if op.get_id_servico() else None

                    nome_cliente = cliente.get_nome() if cliente else "—"
                    desc_servico = servico.get_descricao() if servico else "—"
                    nome_profissional = getattr(op, "profissional_nome", "—")

                    View.horario_excluir(op.get_id())
                    st.success(
                        f"Horário excluído: cliente '{nome_cliente}', serviço '{desc_servico}', profissional '{nome_profissional}'."
                    )
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao excluir horário: {e}")
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
