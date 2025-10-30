import json
from abc import ABC, abstractmethod

class DAO(ABC):
    __objetos = []

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        novo_id = max([o.get_id() for o in cls.__objetos], default=0) + 1
        obj.set_id(novo_id)
        cls.__objetos.append(obj)
        cls.salvar()

    @classmethod
    def listar(cls):
        cls.abrir()
        return cls.__objetos

    @classmethod
    def listar_id(cls, id):
        cls.abrir()
        for obj in cls.__objetos:
            if obj.get_id() == id:
                return obj
        return None

    @classmethod
    def atualizar(cls, obj):
        cls.abrir()
        for i, existente in enumerate(cls.__objetos):
            if existente.get_id() == obj.get_id():
                cls.__objetos[i] = obj
                cls.salvar()
                return True
        return False

    @classmethod
    def excluir(cls, obj):
        cls.abrir()
        cls.__objetos = [o for o in cls.__objetos if o.get_id() != obj.get_id()]
        cls.salvar()

    @classmethod
    @abstractmethod
    def abrir(cls):
        pass

    @classmethod
    @abstractmethod
    def salvar(cls):
        pass
