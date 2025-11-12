import streamlit as st
import json
from pathlib import Path
from views import View

BASE_DIR = Path(__file__).resolve().parent.parent
USUARIO_FILE = BASE_DIR / "usuario_logado.json"


def carregar_usuario_logado():
    """Lê o usuário atualmente logado do arquivo JSON."""
    if not USUARIO_FILE.exists():
        return None
    try:
        with open(USUARIO_FILE, "r", encoding="utf-8") as f:
            usuarios = json.load(f)
            return usuarios[0] if usuarios else None
    except json.JSONDecodeError:
        return None


class PerfilAdminUI:
    """Permite ao administrador visualizar e atualizar seus próprios dados."""

    @staticmethod
    def main():
        st.header("Meus Dados (Administrador)")

        try:
            usuario = carregar_usuario_logado()
            if not usuario or usuario.get("tipo") != "admin":
                st.warning("Nenhum administrador logado.")
                return

            usuario_id = usuario["id"]

            # ✅ Busca os dados do admin corretamente via View
            admin = View.cliente_listar_id(usuario_id)
            if not admin:
                st.warning("Dados do administrador não encontrados.")
                return

            nome_atual = admin.get_nome()
            email_atual = admin.get_email()
            fone_atual = admin.get_fone()
            senha_atual = admin.get_senha()

            with st.form("form_atualizar_admin"):
                nome = st.text_input("Nome", nome_atual)
                email = st.text_input("E-mail (não pode ser alterado)", email_atual, disabled=True)
                fone = st.text_input("Telefone", fone_atual)
                nova_senha = st.text_input("Nova senha (deixe vazio para manter a atual)", type="password")
                senha_final = nova_senha if nova_senha else senha_atual

                submitted = st.form_submit_button("Atualizar Dados")

                if submitted:
                    try:
                        if not nome.strip():
                            raise ValueError("O nome é obrigatório.")

                        # ✅ Atualiza o cadastro do admin corretamente
                        View.cliente_atualizar(usuario_id, nome, email_atual, fone, senha_final)

                        # Atualiza o JSON de login
                        usuario["nome"] = nome
                        usuario["fone"] = fone
                        with open(USUARIO_FILE, "w", encoding="utf-8") as f:
                            json.dump([usuario], f, indent=4, ensure_ascii=False)

                        st.success("Dados do administrador atualizados com sucesso!")

                    except ValueError as ve:
                        st.error(f"Erro de validação: {ve}")
                    except Exception as e:
                        st.error(f"Erro ao atualizar dados do administrador: {e}")

        except Exception as e:
            st.error(f"Erro ao carregar o perfil do administrador: {e}")
