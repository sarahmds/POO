import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
from models.cliente import Cliente, ClienteDAO
from models.servico import Servico, ServicoDAO
from models.horario import Horario, HorarioDAO
from models.profissional import Profissional, ProfissionalDAO

class View:
    ARQUIVO_HORARIOS = Path(__file__).resolve().parent.parent / "horarios.json"

    # ----------------------------------------------------------------
    # CLIENTE
    # ----------------------------------------------------------------
    @staticmethod
    def cliente_criar_admin():
        for c in View.cliente_listar():
            if c.get_email() == "admin":
                return
        View.cliente_inserir("admin", "admin", "fone", "1234")

    @staticmethod
    def cliente_inserir(nome, email, fone, senha):
        if not nome or not email or not senha:
            raise ValueError("Nome, e-mail e senha são obrigatórios.")
        email_lower = email.lower()
        todos_emails = [c.get_email().lower() for c in ClienteDAO.listar()] + \
                       [p.get_email().lower() for p in ProfissionalDAO.listar()]
        if email_lower in todos_emails:
            raise ValueError("Já existe um usuário com esse e-mail.")
        ClienteDAO.inserir(Cliente(0, nome, email, fone, senha))

    @staticmethod
    def cliente_atualizar(id, nome, email, fone, senha):
        if not nome or not email or not senha:
            raise ValueError("Nome, e-mail e senha são obrigatórios.")
        email_lower = email.lower()
        todos_emails = [c.get_email().lower() for c in ClienteDAO.listar() if c.get_id() != id] + \
                       [p.get_email().lower() for p in ProfissionalDAO.listar()]
        if email_lower in todos_emails:
            raise ValueError("Já existe um usuário com esse e-mail.")
        ClienteDAO.atualizar(Cliente(id, nome, email, fone, senha))

    @staticmethod
    def cliente_excluir(id):
        horarios_cliente = [h for h in HorarioDAO.listar() if h.get_id_cliente() == id]
        if horarios_cliente:
            raise ValueError("Não é possível excluir clientes que tenham horários agendados.")
        cliente = ClienteDAO.listar_id(id)
        if not cliente:
            raise ValueError("Cliente não encontrado.")
        ClienteDAO.excluir(cliente)

    @staticmethod
    def cliente_listar() -> List[Cliente]:
        return ClienteDAO.listar()

    @staticmethod
    def cliente_listar_id(id) -> Optional[Cliente]:
        return ClienteDAO.listar_id(id)

    @staticmethod
    def cliente_autenticar(email: str, senha: str) -> Optional[Dict[str, Any]]:
        return ClienteDAO.autenticar(email, senha)

    # ----------------------------------------------------------------
    # PROFISSIONAL
    # ----------------------------------------------------------------
    @staticmethod
    def profissional_inserir(nome, especialidade, conselho, email, senha):
        if not nome or not email or not senha:
            raise ValueError("Nome, e-mail e senha são obrigatórios.")
        email_lower = email.lower()
        if email_lower == "admin":
            raise ValueError("O e-mail 'admin' é reservado para o administrador.")
        todos_emails = [c.get_email().lower() for c in ClienteDAO.listar()] + \
                       [p.get_email().lower() for p in ProfissionalDAO.listar()]
        if email_lower in todos_emails:
            raise ValueError("Já existe um usuário com esse e-mail.")
        ProfissionalDAO.inserir(Profissional(0, nome, especialidade, conselho, email, senha))

    @staticmethod
    def profissional_atualizar(id, nome, especialidade, conselho, email, senha):
        if not nome or not email or not senha:
            raise ValueError("Nome, e-mail e senha são obrigatórios.")
        email_lower = email.lower()
        if email_lower == "admin":
            raise ValueError("O e-mail 'admin' é reservado para o administrador.")
        todos_emails = [c.get_email().lower() for c in ClienteDAO.listar()] + \
                       [p.get_email().lower() for p in ProfissionalDAO.listar() if p.get_id() != id]
        if email_lower in todos_emails:
            raise ValueError("Já existe um usuário com esse e-mail.")
        ProfissionalDAO.atualizar(Profissional(id, nome, especialidade, conselho, email, senha))

    @staticmethod
    def profissional_excluir(id):
        horarios_prof = [h for h in HorarioDAO.listar() if h.get_id_profissional() == id]
        if horarios_prof:
            raise ValueError("Não é possível excluir profissionais que tenham horários cadastrados.")
        profissional = ProfissionalDAO.listar_id(id)
        if not profissional:
            raise ValueError("Profissional não encontrado.")
        ProfissionalDAO.excluir(profissional)

    @staticmethod
    def profissional_listar() -> List[Profissional]:
        return ProfissionalDAO.listar()

    @staticmethod
    def profissional_listar_id(id) -> Optional[Profissional]:
        return ProfissionalDAO.listar_id(id)

    @staticmethod
    def profissional_autenticar(email: str, senha: str) -> Optional[Dict[str, Any]]:
        return ProfissionalDAO.autenticar(email, senha)

    # ----------------------------------------------------------------
    # SERVIÇO
    # ----------------------------------------------------------------
    @staticmethod
    def servico_inserir(descricao: str, preco: float):
        ServicoDAO.inserir(Servico(0, descricao, preco))

    @staticmethod
    def servico_listar() -> List[Servico]:
        return ServicoDAO.listar()

    @staticmethod
    def servico_listar_id(id: int) -> Optional[Servico]:
        return ServicoDAO.listar_id(id)

    @staticmethod
    def servico_atualizar(id: int, descricao: str, preco: float):
        ServicoDAO.atualizar(Servico(id, descricao, preco))

    @staticmethod
    def servico_excluir(id: int):
        ServicoDAO.excluir(Servico(id, "", 0.0))

    # ----------------------------------------------------------------
    # HORÁRIOS
    # ----------------------------------------------------------------
    @staticmethod
    def horario_inserir(data, confirmado, id_cliente, id_servico, id_profissional):
        horarios_existentes = [h for h in HorarioDAO.listar()
                               if h.get_id_profissional() == id_profissional and h.get_data() == data]
        if horarios_existentes:
            raise ValueError("Já existe um horário para este profissional na mesma data e hora.")
        h = Horario(0, data)
        h.set_confirmado(confirmado)
        h.set_id_cliente(id_cliente)
        h.set_id_servico(id_servico)
        h.set_id_profissional(id_profissional)
        prof = ProfissionalDAO.listar_id(id_profissional)
        h.profissional_nome = prof.get_nome() if prof else "—"
        HorarioDAO.inserir(h)
        HorarioDAO.salvar()

    @staticmethod
    def horario_atualizar(id, data, confirmado, id_cliente, id_servico, id_profissional):
        horarios_existentes = [h for h in HorarioDAO.listar()
                               if h.get_id() != id and h.get_id_profissional() == id_profissional and h.get_data() == data]
        if horarios_existentes:
            raise ValueError("Já existe um horário para este profissional na mesma data e hora.")
        h = Horario(id, data)
        h.set_confirmado(confirmado)
        h.set_id_cliente(id_cliente)
        h.set_id_servico(id_servico)
        h.set_id_profissional(id_profissional)
        prof = ProfissionalDAO.listar_id(id_profissional)
        h.profissional_nome = prof.get_nome() if prof else "—"
        HorarioDAO.atualizar(h)
        HorarioDAO.salvar()

    @staticmethod
    def horario_excluir(id):
        from templates.loginUI import carregar_usuario
        h = HorarioDAO.listar_id(id)
        if h is None:
            raise ValueError("Horário não encontrado.")
        usuario = carregar_usuario()
        tipo = usuario.get("tipo") if usuario else None
        if tipo != "admin" and h.get_id_cliente() != 0 and h.get_confirmado():
            raise ValueError("Não é possível excluir horários já agendados por um cliente.")
        HorarioDAO.excluir(h)
        HorarioDAO.salvar()

    @staticmethod
    def horario_listar() -> List[Horario]:
        """Lista horários do banco e também do JSON (agenda aberta dos profissionais)."""
        horarios = HorarioDAO.listar()
        if View.ARQUIVO_HORARIOS.exists():
            with open(View.ARQUIVO_HORARIOS, "r", encoding="utf-8") as f:
                try:
                    dados_json = json.load(f)
                    for item in dados_json:
                        h = Horario(
                            item.get("id", 0),
                            datetime.strptime(item.get("data"), "%d/%m/%Y %H:%M")
                            if "data" in item and item["data"] else datetime.now()
                        )
                        h.set_confirmado(str(item.get("confirmado")).lower() in ["true", "1", "sim"])
                        h.set_id_cliente(item.get("id_cliente", 0))
                        h.set_id_servico(item.get("id_servico", 0))
                        h.set_id_profissional(item.get("id_profissional", 0))
                        h.profissional_nome = item.get("profissional_nome", "—")
                        horarios.append(h)
                except json.JSONDecodeError:
                    pass
        return horarios
