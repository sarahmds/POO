import streamlit as st
import pandas as pd
from datetime import datetime
import time
from views import View
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

    # ===============================
    # LISTAR
    # ===============================
    @staticmethod
    def listar():
        try:
            usuario = carregar_usuario()
            if not usuario:
                st.error("Usuário não autenticado.")
                return

            horarios = View.horario_listar()
            dados = []

            def safe_int(val):
                try:
                    return int(val)
                except (TypeError, ValueError):
                    return None

            for obj in horarios:
                id_cliente = safe_int(obj.get_id_cliente())
                id_servico = safe_int(obj.get_id_servico())
                id_profissional = safe_int(obj.get_id_profissional())

                # Buscar objetos completos via View (sem ler JSON diretamente)
                cliente_obj = View.cliente_listar_id(id_cliente) if id_cliente else None
                servico_obj = View.servico_listar_id(id_servico) if id_servico else None
                profissional_obj = View.profissional_listar_id(id_profissional) if id_profissional else None

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
                    "Profissional": profissional_obj.get_nome() if profissional_obj else "—"
                })

            if not dados:
                st.info("Nenhum horário encontrado para o seu usuário.")
                return

            df = pd.DataFrame(dados, columns=["ID", "Data", "Confirmado", "Cliente", "Serviço", "Profissional"])
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao listar horários: {e}")

    # ===============================
    # INSERIR
    # ===============================
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
            cliente = st.selectbox("Cliente", clientes, format_func=lambda c: c.get_nome())
            servico = st.selectbox("Serviço", servicos, format_func=lambda s: s.get_descricao())
            profissional = st.selectbox("Profissional", profissionais, format_func=lambda p: p.get_nome())

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

    # ===============================
    # ATUALIZAR
    # ===============================
    @staticmethod
    def atualizar():
        try:
            usuario = carregar_usuario()
            if not usuario:
                st.error("Usuário não autenticado.")
                return

            if usuario["tipo"] == "cliente":
                st.warning("Clientes não podem atualizar horários pelo painel.")
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
            cliente = st.selectbox("Novo cliente", clientes, index=cliente_index, format_func=lambda c: c.get_nome())
            servico = st.selectbox("Novo serviço", servicos, index=servico_index, format_func=lambda s: s.get_descricao())
            profissional = st.selectbox("Novo profissional", profissionais, index=profissional_index, format_func=lambda p: p.get_nome())

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

    # ===============================
    # EXCLUIR
    # ===============================
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
                    profissional = View.profissional_listar_id(op.get_id_profissional()) if op.get_id_profissional() else None

                    nome_cliente = cliente.get_nome() if cliente else "—"
                    desc_servico = servico.get_descricao() if servico else "—"
                    nome_profissional = profissional.get_nome() if profissional else "—"

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
