from models.cliente import Cliente, ClienteDAO
from models.servico import Servico, ServicoDAO
from models.horario import Horario, HorarioDAO
from models.profissional import Profissional, ProfissionalDAO
from datetime import datetime

class View:

    # ---------------------- CLIENTE ----------------------
    @staticmethod
    def cliente_inserir(nome, email, fone):
        ClienteDAO.inserir(Cliente(0, nome, email, fone))

    @staticmethod
    def cliente_listar():
        return ClienteDAO.listar()

    @staticmethod
    def cliente_listar_id(id):
        return ClienteDAO.listar_id(id)

    @staticmethod
    def cliente_atualizar(id, nome, email, fone):
        ClienteDAO.atualizar(Cliente(id, nome, email, fone))

    @staticmethod
    def cliente_excluir(id):
        ClienteDAO.excluir(Cliente(id, "", "", ""))


    # ---------------------- SERVIÇO ----------------------
    @staticmethod
    def servico_inserir(descricao, preco):
        ServicoDAO.inserir(Servico(0, descricao, preco))

    @staticmethod
    def servico_listar():
        return ServicoDAO.listar()

    @staticmethod
    def servico_listar_id(id):
        return ServicoDAO.listar_id(id)

    @staticmethod
    def servico_atualizar(id, descricao, preco):
        ServicoDAO.atualizar(Servico(id, descricao, preco))

    @staticmethod
    def servico_excluir(id):
        ServicoDAO.excluir(Servico(id, "", 0.0))


 # ---------------------- HORÁRIO ----------------------
    @staticmethod
    def horario_inserir(data, confirmado, id_cliente, id_servico, id_profissional):
        c = Horario(0, data)
        c.set_confirmado(confirmado)
        c.set_id_cliente(id_cliente)
        c.set_id_servico(id_servico)
        c.set_id_profissional(id_profissional)
        HorarioDAO.inserir(c)

    @staticmethod
    def horario_listar():
        return HorarioDAO.listar()

    @staticmethod
    def horario_atualizar(id, data, confirmado, id_cliente, id_servico, id_profissional):
        c = Horario(id, data)
        c.set_confirmado(confirmado)
        c.set_id_cliente(id_cliente)
        c.set_id_servico(id_servico)
        c.set_id_profissional(id_profissional)
        HorarioDAO.atualizar(c)

    @staticmethod
    def horario_excluir(id):
        HorarioDAO.excluir(Horario(id, None))
   # ---------------------- PROFISSIONAL ----------------------
@staticmethod
def profissional_inserir(nome, profissao, email, senha):
    """
    Insere um novo profissional com nome, profissão, email e senha.
    """
    ProfissionalDAO.inserir(Profissional(0, nome, profissao, email, senha))

@staticmethod
def profissional_listar():
    return ProfissionalDAO.listar()

@staticmethod
def profissional_listar_id(id):
    return ProfissionalDAO.listar_id(id)

@staticmethod
def profissional_atualizar(id, nome, profissao, email, senha):
    ProfissionalDAO.atualizar(Profissional(id, nome, profissao, email, senha))

@staticmethod
def profissional_excluir(id):
    ProfissionalDAO.excluir(Profissional(id, "", "", "", ""))

@staticmethod
def profissional_autenticar(email, senha):
    """
    Autenticação via email e senha.
    Retorna True se existir um profissional com email e senha fornecidos.
    """
    for prof in ProfissionalDAO.listar():
        if prof.get_email() == email and prof.get_senha() == senha:
            return True
    return False
