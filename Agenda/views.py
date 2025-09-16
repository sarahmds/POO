from models.cliente import Cliente, ClienteDAO
from models.servico import Servico, ServicoDAO  

class View:

    # ---- CLIENTES ----
    def cliente_inserir(nome, email, fone):
        cliente = Cliente(0, nome, email, fone)
        ClienteDAO.inserir(cliente)

    def cliente_listar():
        return ClienteDAO.listar()
  
    def cliente_listar_id(id):
        return ClienteDAO.listar_id(id)

    def cliente_atualizar(id, nome, email, fone):
        cliente = Cliente(id, nome, email, fone)
        ClienteDAO.atualizar(cliente)
    
    def cliente_excluir(id):
        cliente = Cliente(id, "", "", "")
        ClienteDAO.excluir(cliente)    

    # ---- SERVIÇOS ----
    def servico_listar():
        return ServicoDAO.listar()

    def servico_inserir(descricao, preco):
        servico = Servico(0, descricao, preco)
        ServicoDAO.inserir(servico)

    def servico_atualizar(id, descricao, preco):
        servico = Servico(id, descricao, preco)
        ServicoDAO.atualizar(servico)

    def servico_excluir(id):
        servico = Servico(id, "", 0)
        ServicoDAO.excluir(servico)
