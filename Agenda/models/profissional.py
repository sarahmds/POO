from dataclasses import dataclass

class Profissional:
    def __init__(self, id, nome, telefone=""):
        self.set_id(id)
        self.set_nome(nome)
        self.set_telefone(telefone)

    def __str__(self):
        return f"{self.__id} - {self.__nome}"

    def get_id(self):
        return self.__id

    def get_nome(self):
        return self.__nome

    def get_telefone(self):
        return self.__telefone

    def set_id(self, id):
        self.__id = id

    def set_nome(self, nome):
        self.__nome = nome

    def set_telefone(self, telefone):
        self.__telefone = telefone

    def to_json(self):
        return {"id": self.__id, "nome": self.__nome, "telefone": self.__telefone}

    @staticmethod
    def from_json(dic):
        p = Profissional(dic["id"], dic.get("nome", ""), dic.get("telefone", ""))
        return p
