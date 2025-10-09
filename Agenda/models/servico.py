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

class ServicoDAO:
    __objetos = []

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        novo_id = max([s.get_id() for s in cls.__objetos], default=0) + 1
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
        cls.__objetos = [s for s in cls.__objetos if s.get_id() != obj.get_id()]
        cls.salvar()

    @classmethod
    def abrir(cls):
        cls.__objetos = []
        try:
            with open("servicos.json", mode="r", encoding="utf-8") as arquivo:
                lista_dicts = json.load(arquivo)
                for dic in lista_dicts:
                    servico = Servico.from_json(dic)
                    cls.__objetos.append(servico)
        except (FileNotFoundError, json.JSONDecodeError):
            cls.__objetos = []

    @classmethod
    def salvar(cls):
        with open("servicos.json", mode="w", encoding="utf-8") as arquivo:
            json.dump([Servico.to_json(s) for s in cls.__objetos], arquivo, ensure_ascii=False, indent=4)
