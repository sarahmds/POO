import streamlit as st
import json
from pathlib import Path
from views import View

BASE_DIR = Path(__file__).resolve().parent.parent
USUARIO_FILE = BASE_DIR / "usuario_logado.json"


def carregar_usuario_logado():
    """Carrega o usuário logado a partir do JSON."""
    if not USUARIO_FILE.exists():
        return None
    try:
        with open(USUARIO_FILE, "r", encoding="utf-8") as f:
            usuarios = json.load(f)
            return usuarios[0] if usuarios else None
    except json.JSONDecodeError:
        return None


class PerfilProfissionalUI:
    """Interface para visualização e atualização do perfil do profissional."""

    @staticmethod
    def main():
        st.header("Meus Dados (Profissional)")

        try:
            usuario = carregar_usuario_logado()
            if not usuario or usuario.get("tipo") != "profissional":
                st.warning("Nenhum profissional logado.")
                return

            usuario_id = usuario["id"]

            # Carrega o profissional via View
            profissional = View.profissional_listar_id(usuario_id)
            if not profissional:
                st.warning("Dados do profissional não encontrados.")
                return

            # Dados atuais
            nome_atual = profissional.get_nome()
            especialidade_atual = profissional.get_especialidade()
            conselho_atual = profissional.get_conselho()
            email_atual = profissional.get_email()
            senha_atual = profissional.get_senha()

            # Verifica se é admin para desabilitar edição do e-mail
            eh_admin = email_atual.lower() == "admin@admin.com"

            # Formulário de atualização
            with st.form("form_atualizar_profissional"):
                nome = st.text_input("Nome", nome_atual)
                especialidade = st.text_input("Especialidade", especialidade_atual)
                conselho = st.text_input("Conselho", conselho_atual)
                email = st.text_input(
                    "E-mail" if not eh_admin else "E-mail (não pode ser alterado)",
                    email_atual,
                    disabled=eh_admin
                )
                nova_senha = st.text_input("Nova senha (deixe vazio para manter a atual)", type="password")
                senha_final = nova_senha if nova_senha else senha_atual

                submitted = st.form_submit_button("Atualizar Dados")

                if submitted:
                    try:
                        if not nome.strip() or not especialidade.strip() or not email_atual.strip():
                            raise ValueError("Nome, especialidade e e-mail são obrigatórios.")

                        # Atualiza via View
                        View.profissional_atualizar(
                            usuario_id,
                            nome,
                            especialidade,
                            conselho,
                            email_atual,
                            senha_final
                        )

                        # Atualiza informações básicas no JSON de login
                        usuario["nome"] = nome
                        usuario["especialidade"] = especialidade
                        usuario["conselho"] = conselho

                        with open(USUARIO_FILE, "w", encoding="utf-8") as f:
                            json.dump([usuario], f, indent=4, ensure_ascii=False)

                        st.success("Dados do profissional atualizados com sucesso!")

                    except ValueError as ve:
                        st.error(f"Erro de validação: {ve}")
                    except Exception as e:
                        st.error(f"Erro ao atualizar dados do profissional: {e}")

        except Exception as e:
            st.error(f"Erro ao carregar perfil do profissional: {e}")
