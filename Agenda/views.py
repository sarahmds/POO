from models.cliente import Cliente, ClienteDAO
from models.servico import Servico, ServicoDAO
from models.horario import Horario, HorarioDAO
from models.profissional import Profissional, ProfissionalDAO
from datetime import datetime

class View:

    def cliente_inserir(nome, email, fone):
        ClienteDAO.inserir(Cliente(0, nome, email, fone))
    def cliente_listar(): return ClienteDAO.listar()
    def cliente_listar_id(id): return ClienteDAO.listar_id(id)
    def cliente_atualizar(id, nome, email, fone): ClienteDAO.atualizar(Cliente(id, nome, email, fone))
    def cliente_excluir(id): ClienteDAO.excluir(Cliente(id, "", "", ""))


    def servico_inserir(descricao, preco): ServicoDAO.inserir(Servico(0, descricao, preco))
    def servico_listar(): return ServicoDAO.listar()
    def servico_listar_id(id): return ServicoDAO.listar_id(id)
    def servico_atualizar(id, descricao, preco): ServicoDAO.atualizar(Servico(id, descricao, preco))
    def servico_excluir(id): ServicoDAO.excluir(Servico(id, "", 0))


    def horario_inserir(data, confirmado, id_cliente, id_servico, id_profissional):
        c = Horario(0, data)
        c.set_confirmado(confirmado)
        c.set_id_cliente(id_cliente)
        c.set_id_servico(id_servico)
        c.set_id_profissional(id_profissional)
        HorarioDAO.inserir(c)

    def horario_listar(): return HorarioDAO.listar()
    def horario_atualizar(id, data, confirmado, id_cliente, id_servico, id_profissional):
        c = Horario(id, data)
        c.set_confirmado(confirmado)
        c.set_id_cliente(id_cliente)
        c.set_id_servico(id_servico)
        c.set_id_profissional(id_profissional)
        HorarioDAO.atualizar(c)

    def horario_excluir(id): HorarioDAO.excluir(Horario(id, None))


    def profissional_inserir(nome, profissao): ProfissionalDAO.inserir(Profissional(0, nome, profissao))
    def profissional_listar(): return ProfissionalDAO.listar()
    def profissional_listar_id(id): return ProfissionalDAO.listar_id(id)
    def profissional_atualizar(id, nome, profissao): ProfissionalDAO.atualizar(Profissional(id, nome, profissao))
    def profissional_excluir(id): ProfissionalDAO.excluir(Profissional(id, "", ""))
