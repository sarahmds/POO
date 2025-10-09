from models.cliente import Cliente, ClienteDAO
from models.servico import Servico, ServicoDAO
from models.horario import Horario, HorarioDAO
from models.profissional import Profissional, ProfissionalDAO
from typing import Optional, Dict, Any

class View:


    @staticmethod
    def cliente_inserir(nome, email, fone, senha):
        ClienteDAO.inserir(Cliente(0, nome, email, fone, senha)) 

    @staticmethod
    def cliente_listar():
        return ClienteDAO.listar()

    @staticmethod
    def cliente_listar_id(id):
        return ClienteDAO.listar_id(id)

    @staticmethod
    def cliente_atualizar(id, nome, email, fone, senha):
        ClienteDAO.atualizar(Cliente(id, nome, email, fone, senha))

    @staticmethod
    def cliente_excluir(id):
        ClienteDAO.excluir(Cliente(id, "", "", "", ""))

    @staticmethod
    def cliente_autenticar(email: str, senha: str) -> Optional[Dict[str, Any]]:
        return ClienteDAO.autenticar(email, senha)



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


    @staticmethod
    def profissional_inserir(nome, especialidade, conselho, email, senha):
        ProfissionalDAO.inserir(Profissional(0, nome, especialidade, conselho, email, senha))

    @staticmethod
    def profissional_listar():
        return ProfissionalDAO.listar()

    @staticmethod
    def profissional_listar_id(id):
        return ProfissionalDAO.listar_id(id)

    @staticmethod
    def profissional_atualizar(id, nome, especialidade, conselho, email, senha):
        ProfissionalDAO.atualizar(Profissional(id, nome, especialidade, conselho, email, senha))

    @staticmethod
    def profissional_excluir(id):
        ProfissionalDAO.excluir(Profissional(id, "", "", "", "", ""))

    @staticmethod
    def profissional_autenticar(email: str, senha: str) -> Optional[Dict[str, Any]]:
        return ProfissionalDAO.autenticar(email, senha)
