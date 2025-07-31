from modelo.contato import Contato
from dao.contato_dao import ContatoDAO

class ContatoView:
    @staticmethod
    def cliente_inserir(id, nome, email, fone, nascimento):
        contato = Contato(id, nome, email, fone, nascimento)
        ContatoDAO.inserir(contato)

    @staticmethod
    def cliente_listar():
        return ContatoDAO.listar()

    @staticmethod
    def cliente_listar_id(id):
        return ContatoDAO.listar_id(id)

    @staticmethod
    def cliente_atualizar(id, nome, email, fone, nascimento):
        contato = Contato(id, nome, email, fone, nascimento)
        return ContatoDAO.atualizar(contato)

    @staticmethod
    def cliente_excluir(id):
        return ContatoDAO.excluir(id)
