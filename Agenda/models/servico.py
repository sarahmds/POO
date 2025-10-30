import json

class Servico:
    def __init__(self, id, descricao, preco):
        self.set_id(id)
        self.set_descricao(descricao)
        self.set_preco(preco)

    def get_id(self): return self.__id
    def get_descricao(self): return self.__descricao
    def get_preco(self): return self.__preco

    def set_id(self, id): self.__id = id
    def set_descricao(self, descricao): self.__descricao = descricao
    def set_preco(self, preco): self.__preco = preco

    def to_json(self):
        dic = {"id": self.__id, "descricao": self.__descricao, "preco": self.__preco}
        return dic

    @staticmethod
    def from_json(dic):
        return Servico(dic["id"], dic["descricao"], dic["preco"])

    def __str__(self):
        return f"{self.__id} - {self.__descricao} - {self.__preco}"

from .dao import DAO
import json

class ServicoDAO(DAO):

    @classmethod
    def abrir(cls):
        cls._DAO__objetos = []
        try:
            with open("servicos.json", "r", encoding="utf-8") as arquivo:
                lista_dicts = json.load(arquivo)
                from .servico import Servico
                for dic in lista_dicts:
                    servico = Servico.from_json(dic)
                    cls._DAO__objetos.append(servico)
        except (FileNotFoundError, json.JSONDecodeError):
            cls._DAO__objetos = []

    @classmethod
    def salvar(cls):
        with open("servicos.json", "w", encoding="utf-8") as arquivo:
            json.dump([s.to_json() for s in cls._DAO__objetos], arquivo, ensure_ascii=False, indent=4)
