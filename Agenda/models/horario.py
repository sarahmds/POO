import json
from datetime import datetime

class Horario:

    def __init__(self, id, data):
        self.set_id(id)
        self.set_data(data)
        self.set_confirmado(False)
        self.set_id_cliente(0)
        self.set_id_servico(0)
        self.set_id_profissional(0) 


    def get_id(self): return self.__id
    def get_data(self): return self.__data
    def get_confirmado(self): return self.__confirmado
    def get_id_cliente(self): return self.__id_cliente
    def get_id_servico(self): return self.__id_servico
    def get_id_profissional(self): return self.__id_profissional


    def set_id(self, id): self.__id = id
    def set_data(self, data): self.__data = data
    def set_confirmado(self, confirmado): self.__confirmado = confirmado
    def set_id_cliente(self, id_cliente): self.__id_cliente = id_cliente
    def set_id_servico(self, id_servico): self.__id_servico = id_servico
    def set_id_profissional(self, id_profissional): self.__id_profissional = id_profissional

 
    def to_json(self):
        return {
            "id": self.__id,
            "data": self.__data.strftime("%d/%m/%Y %H:%M"),
            "confirmado": self.__confirmado,
            "id_cliente": self.__id_cliente,
            "id_servico": self.__id_servico,
            "id_profissional": self.__id_profissional
        }

    @staticmethod
    def from_json(dic):
        horario = Horario(
            dic["id"], 
            datetime.strptime(dic["data"], "%d/%m/%Y %H:%M")
        )
        horario.set_confirmado(dic["confirmado"])
        horario.set_id_cliente(dic["id_cliente"])
        horario.set_id_servico(dic["id_servico"])
        horario.set_id_profissional(dic.get("id_profissional", 0))
        return horario

    def __str__(self):
        return f"{self.__id} - {self.__data.strftime('%d/%m/%Y %H:%M')} - Confirmado: {self.__confirmado}"



class HorarioDAO:

    __objetos = []

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        novo_id = max([h.get_id() for h in cls.__objetos], default=0) + 1
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
        cls.__objetos = [h for h in cls.__objetos if h.get_id() != obj.get_id()]
        cls.salvar()

    @classmethod
    def abrir(cls):
        cls.__objetos = []
        try:
            with open("horarios.json", "r", encoding="utf-8") as arquivo:
                lista_dicts = json.load(arquivo)
                for dic in lista_dicts:
                    horario = Horario.from_json(dic)
                    cls.__objetos.append(horario)
        except (FileNotFoundError, json.JSONDecodeError):
            cls.__objetos = []

    @classmethod
    def salvar(cls):
        with open("horarios.json", "w", encoding="utf-8") as arquivo:
            json.dump([h.to_json() for h in cls.__objetos], arquivo, ensure_ascii=False, indent=4)