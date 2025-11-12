import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
from models.cliente import Cliente, ClienteDAO
from models.profissional import Profissional, ProfissionalDAO
from models.servico import Servico, ServicoDAO
from models.horario import Horario, HorarioDAO

class View:
    ARQUIVO_HORARIOS = Path(__file__).resolve().parent.parent / "horarios.json"

    # ============================================================
    # CLIENTE
    # ============================================================
    @staticmethod
    def cliente_listar_id(id: int) -> Optional[Cliente]:
        return ClienteDAO.listar_id(id)

    @staticmethod
    def cliente_autenticar(email: str, senha: str) -> Optional[Dict[str, Any]]:
        return ClienteDAO.autenticar(email, senha)

    @staticmethod
    def cliente_criar_admin():
        try:
            for c in ClienteDAO.listar():
                if c.get_email().lower() == "admin@admin.com":
                    return
            cliente_admin = Cliente(0, "Administrador", "admin@admin.com", "(00) 00000-0000", "admin")
            ClienteDAO.inserir(cliente_admin)
            ClienteDAO.salvar()
        except Exception as e:
            print(f"Erro ao criar admin: {e}")

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
        ClienteDAO.salvar()

    @staticmethod
    def cliente_atualizar(id, nome, email, fone, senha):
        cliente_existente = ClienteDAO.listar_id(id)
        if not cliente_existente:
            raise ValueError("Cliente não encontrado.")
        cliente_existente.set_nome(nome)
        cliente_existente.set_email(email)
        cliente_existente.set_fone(fone)
        cliente_existente.set_senha(senha)
        ClienteDAO.atualizar(cliente_existente)
        ClienteDAO.salvar()

    @staticmethod
    def cliente_excluir(id):
        horarios_cliente = [h for h in HorarioDAO.listar() if h.get_id_cliente() == id]
        if horarios_cliente:
            raise ValueError("Não é possível excluir clientes com horários agendados.")
        cliente = ClienteDAO.listar_id(id)
        if not cliente:
            raise ValueError("Cliente não encontrado.")
        ClienteDAO.excluir(cliente)
        ClienteDAO.salvar()

    @staticmethod
    def cliente_listar():
        return ClienteDAO.listar()

    # ============================================================
    # PROFISSIONAL
    # ============================================================
    @staticmethod
    def profissional_listar():
        return ProfissionalDAO.listar()

    @staticmethod
    def profissional_listar_id(id):
        return ProfissionalDAO.listar_id(id)

    @staticmethod
    def profissional_autenticar(email: str, senha: str) -> Optional[Dict[str, Any]]:
        return ProfissionalDAO.autenticar(email, senha)

    @staticmethod
    def profissional_inserir(nome, especialidade, conselho, email, senha):
        if not nome or not email or not senha:
            raise ValueError("Nome, e-mail e senha são obrigatórios.")
        email_lower = email.lower()
        if email_lower == "admin@admin.com":
            raise ValueError("O e-mail 'admin@admin.com' é reservado para o administrador.")
        todos_emails = [c.get_email().lower() for c in ClienteDAO.listar()] + \
                       [p.get_email().lower() for p in ProfissionalDAO.listar()]
        if email_lower in todos_emails:
            raise ValueError("Já existe um usuário com esse e-mail.")
        ProfissionalDAO.inserir(Profissional(0, nome, especialidade, conselho, email, senha))
        ProfissionalDAO.salvar()

    @staticmethod
    def profissional_atualizar(id, nome, especialidade, conselho, email, senha):
        profissional_existente = ProfissionalDAO.listar_id(id)
        if not profissional_existente:
            raise ValueError("Profissional não encontrado.")
        email_lower = email.lower()
        if email_lower == "admin@admin.com":
            raise ValueError("O e-mail 'admin@admin.com' é reservado para o administrador.")
        todos_emails = [c.get_email().lower() for c in ClienteDAO.listar()] + \
                       [p.get_email().lower() for p in ProfissionalDAO.listar() if p.get_id() != id]
        if email_lower in todos_emails:
            raise ValueError("Já existe outro usuário com esse e-mail.")
        profissional_existente.set_nome(nome)
        profissional_existente.set_especialidade(especialidade)
        profissional_existente.set_conselho(conselho)
        profissional_existente.set_email(email)
        profissional_existente.set_senha(senha)
        ProfissionalDAO.atualizar(profissional_existente)
        ProfissionalDAO.salvar()

    @staticmethod
    def profissional_excluir(id):
        horarios_prof = [h for h in HorarioDAO.listar() if h.get_id_profissional() == id]
        if horarios_prof:
            raise ValueError("Não é possível excluir profissionais com horários cadastrados.")
        prof = ProfissionalDAO.listar_id(id)
        if not prof:
            raise ValueError("Profissional não encontrado.")
        ProfissionalDAO.excluir(prof)
        ProfissionalDAO.salvar()

    # ============================================================
    # SERVIÇOS
    # ============================================================
    @staticmethod
    def servico_listar() -> List[Servico]:
        return ServicoDAO.listar()

    @staticmethod
    def servico_listar_id(id: int) -> Optional[Servico]:
        return ServicoDAO.listar_id(id)

    @staticmethod
    def servico_inserir(descricao: str, preco: float):
        ServicoDAO.inserir(Servico(0, descricao, preco))
        ServicoDAO.salvar()

    @staticmethod
    def servico_atualizar(id: int, descricao: str, preco: float):
        ServicoDAO.atualizar(Servico(id, descricao, preco))
        ServicoDAO.salvar()

    @staticmethod
    def servico_excluir(id: int):
        ServicoDAO.excluir(Servico(id, "", 0.0))
        ServicoDAO.salvar()

    # ============================================================
    # HORÁRIOS
    # ============================================================
    @staticmethod
    def horario_listar() -> List[Horario]:
        return HorarioDAO.listar()

    @staticmethod
    def horario_listar_disponiveis() -> List[Horario]:
        """Retorna todos os horários disponíveis (id_cliente == 0 ou None)."""
        return [h for h in HorarioDAO.listar() if not h.get_id_cliente()]

    @staticmethod
    def horario_inserir(data, confirmado, id_cliente, id_servico, id_profissional):
        if isinstance(data, str):
            data_obj = datetime.strptime(data, "%d/%m/%Y %H:%M")
        else:
            data_obj = data
        for h in HorarioDAO.listar():
            if h.get_id_profissional() == id_profissional and h.get_data() == data_obj:
                raise ValueError("Já existe um horário para este profissional na mesma data e hora.")
        h = Horario(0, data_obj)
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
        h = HorarioDAO.listar_id(id)
        if not h:
            raise ValueError("Horário não encontrado.")
        if isinstance(data, str):
            data_obj = datetime.strptime(data, "%d/%m/%Y %H:%M")
        else:
            data_obj = data
        h.set_data(data_obj)
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
        h = HorarioDAO.listar_id(id)
        if not h:
            raise ValueError("Horário não encontrado.")
        HorarioDAO.excluir(h)
        HorarioDAO.salvar()
