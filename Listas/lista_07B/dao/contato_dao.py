import json
from modelo.contato import Contato

class ContatoDAO:
    __contatos = []

    @classmethod
    def inserir(cls, contato):
        cls.__abrir()
        cls.__contatos.append(contato)
        cls.__salvar()

    @classmethod
    def listar(cls):
        cls.__abrir()
        return cls.__contatos

    @classmethod
    def listar_id(cls, id):
        cls.__abrir()
        for c in cls.__contatos:
            if c.get_id() == id:
                return c
        return None

    @classmethod
    def atualizar(cls, contato):
        cls.__abrir()
        for i, c in enumerate(cls.__contatos):
            if c.get_id() == contato.get_id():
                cls.__contatos[i] = contato
                cls.__salvar()
                return True
        return False

    @classmethod
    def excluir(cls, id):
        cls.__abrir()
        for i, c in enumerate(cls.__contatos):
            if c.get_id() == id:
                del cls.__contatos[i]
                cls.__salvar()
                return True
        return False

    @classmethod
    def __abrir(cls):
        try:
            with open("clientes.json", "r") as arq:
                dados = json.load(arq)
                cls.__contatos = [Contato(**d) for d in dados]
        except:
            cls.__contatos = []

    @classmethod
    def __salvar(cls):
        with open("clientes.json", "w") as arq:
            dados = [{
                "id": c.get_id(),
                "nome": c.get_nome(),
                "email": c.get_email(),
                "fone": c.get_fone(),
                "nascimento": c.get_nascimento()
            } for c in cls.__contatos]
            json.dump(dados, arq, indent=4)
