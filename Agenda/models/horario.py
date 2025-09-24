import json

class Horario:
    __objetos = []

    def __init__(self, id, outros_atributos=None):
        self.id = id
        # outros atributos aqui
        self.outros_atributos = outros_atributos

    def get_id(self):
        return self.id

    @classmethod
    def listar_id(cls, id):
        for obj in cls.__objetos:
            if obj.get_id() == id:
                return obj
        return None

    @classmethod
    def atualizar(cls, obj):
        aux = cls.listar_id(obj.get_id())
        if aux is not None:
            cls.__objetos.remove(aux)
            cls.__objetos.append(obj)
            cls.salvar()

    @classmethod
    def excluir(cls, obj):
        aux = cls.listar_id(obj.get_id())
        if aux is not None:
            cls.__objetos.remove(aux)
            cls.salvar()

    @classmethod
    def abrir(cls):
        cls.__objetos = []
        try:
            with open("horarios.json", mode="r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    obj = Horario.from_json(dic)
                    cls.__objetos.append(obj)
        except FileNotFoundError:
            pass

    @classmethod
    def salvar(cls):
        with open("horarios.json", mode="w") as arquivo:
            json.dump(cls.__objetos, arquivo, default=Horario.to_json)

    @staticmethod
    def from_json(dic):
        # Cria um objeto Horario a partir de um dicionário
        id = dic.get("id")
        outros_atributos = dic.get("outros_atributos")
        return Horario(id, outros_atributos)

    @staticmethod
    def to_json(obj):
        # Converte um objeto Horario para um dicionário JSON-serializável
        return {
            "id": obj.get_id(),
            "outros_atributos": obj.outros_atributos
        }
