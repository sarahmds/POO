import json

class Profissional:
    def __init__(self, id, nome, profissao):
        self.set_id(id)
        self.set_nome(nome)
        self.set_profissao(profissao)

    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_profissao(self): return self.__profissao

    def set_id(self, id): self.__id = id
    def set_nome(self, nome): self.__nome = nome
    def set_profissao(self, profissao): self.__profissao = profissao

    def to_json(self):
        return {"id": self.__id, "nome": self.__nome, "profissao": self.__profissao}

    @staticmethod
    def from_json(dic):
        return Profissional(dic["id"], dic["nome"], dic["profissao"])

    def __str__(self):
        return f"{self.__id} - {self.__nome} - {self.__profissao}"


class ProfissionalDAO:
    __objetos = []

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        id = 0
        for aux in cls.__objetos:
            if aux.get_id() > id: id = aux.get_id()
        obj.set_id(id + 1)
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
            if obj.get_id() == id: return obj
        return None

    @classmethod
    def atualizar(cls, obj):
        aux = cls.listar_id(obj.get_id())
        if aux != None:
            cls.__objetos.remove(aux)
            cls.__objetos.append(obj)
            cls.salvar()

    @classmethod
    def excluir(cls, obj):
        aux = cls.listar_id(obj.get_id())
        if aux != None:
            cls.__objetos.remove(aux)
            cls.salvar()

    @classmethod
    def abrir(cls):
        cls.__objetos = []
        try:
            with open("profissionais.json", "r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    obj = Profissional.from_json(dic)
                    cls.__objetos.append(obj)
        except FileNotFoundError:
            pass

    @classmethod
    def salvar(cls):
        with open("profissionais.json", "w") as arquivo:
            json.dump(cls.__objetos, arquivo, default=Profissional.to_json)
