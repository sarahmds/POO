import streamlit as st
import json
from pathlib import Path
from views import View

BASE_DIR = Path(__file__).resolve().parent.parent
USUARIO_FILE = BASE_DIR / "usuario_logado.json"


def carregar_usuario_logado():
    """Lê o usuário logado a partir do arquivo JSON."""
    if not USUARIO_FILE.exists():
        return None
    try:
        with open(USUARIO_FILE, "r", encoding="utf-8") as f:
            usuarios = json.load(f)
            return usuarios[0] if usuarios else None
    except json.JSONDecodeError:
        return None


class PerfilClienteUI:
    """Interface de perfil para o cliente logado."""

    @staticmethod
    def main():
        st.header("Meus Dados (Cliente)")

        try:
            usuario = carregar_usuario_logado()
            if not usuario or usuario.get("tipo") != "cliente":
                st.warning("Nenhum cliente logado.")
                return

            usuario_id = usuario["id"]

            # Busca os dados completos do cliente via View
            cliente = View.cliente_listar_id(usuario_id)
            if not cliente:
                st.warning("Dados do cliente não encontrados.")
                return

            nome_atual = cliente.get_nome()
            email_atual = cliente.get_email()
            fone_atual = cliente.get_fone()
            senha_atual = cliente.get_senha()

            with st.form("form_atualizar_cliente"):
                nome = st.text_input("Nome", nome_atual)
                
                # Permite alterar o e-mail, exceto se for o admin
                eh_admin = email_atual.lower() == "admin@admin.com"
                email = st.text_input(
                    "E-mail" if not eh_admin else "E-mail (não pode ser alterado)",
                    email_atual,
                    disabled=eh_admin
                )
                
                fone = st.text_input("Telefone", fone_atual)
                nova_senha = st.text_input(
                    "Nova senha (deixe vazio para manter a atual)", type="password"
                )
                senha_final = nova_senha if nova_senha else senha_atual

                submitted = st.form_submit_button("Atualizar Dados")

                if submitted:
                    try:
                        if not nome.strip() or not email.strip():
                            raise ValueError("Nome e e-mail são obrigatórios.")

                        # Atualiza os dados via View
                        View.cliente_atualizar(usuario_id, nome, email, fone, senha_final)

                        # Atualiza o JSON do usuário logado
                        usuario["nome"] = nome
                        usuario["fone"] = fone
                        usuario["email"] = email
                        with open(USUARIO_FILE, "w", encoding="utf-8") as f:
                            json.dump([usuario], f, indent=4, ensure_ascii=False)

                        st.success("Dados do cliente atualizados com sucesso!")

                    except ValueError as ve:
                        st.error(f"Erro de validação: {ve}")
                    except Exception as e:
                        st.error(f"Erro ao atualizar dados do cliente: {e}")

        except Exception as e:
            st.error(f"Erro ao carregar perfil do cliente: {e}")
