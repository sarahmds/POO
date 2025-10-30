import json
from datetime import datetime
from typing import List, Dict, Any

class HorarioException(Exception):
    """Exceção personalizada para horários inválidos."""
    pass

class Horario:

    def __init__(self, id: int, data: datetime):
        self.set_id(id)
        self.set_data(data)
        self.set_confirmado(False)
        self.set_id_cliente(0)
        self.set_id_servico(0)
        self.set_id_profissional(0)

    def get_id(self) -> int: return self.__id
    def get_data(self) -> datetime: return self.__data
    def get_confirmado(self) -> bool: return self.__confirmado
    def get_id_cliente(self) -> int: return self.__id_cliente
    def get_id_servico(self) -> int: return self.__id_servico
    def get_id_profissional(self) -> int: return self.__id_profissional

    def set_id(self, id: int):
        self.__id = id

    def set_data(self, data: datetime):
        if data.year < 2025:
            raise HorarioException("Horário não pode ter data anterior a 2025.")
        self.__data = data

    def set_confirmado(self, confirmado: bool):
        self.__confirmado = confirmado

    def set_id_cliente(self, id_cliente: int):
        self.__id_cliente = id_cliente

    def set_id_servico(self, id_servico: int):
        self.__id_servico = id_servico

    def set_id_profissional(self, id_profissional: int):
        self.__id_profissional = id_profissional

    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.__id,
            "data": self.__data.strftime("%d/%m/%Y %H:%M"),
            "confirmado": self.__confirmado,
            "id_cliente": self.__id_cliente,
            "id_servico": self.__id_servico,
            "id_profissional": self.__id_profissional
        }

    @staticmethod
    def from_json(dic: Dict[str, Any]):
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


from .dao import DAO
import json

class HorarioDAO(DAO):

    @classmethod
    def abrir(cls):
        cls._DAO__objetos = [] 
        try:
            with open("horarios.json", "r", encoding="utf-8") as arquivo:
                lista_dicts = json.load(arquivo)
                from .horario import Horario
                for dic in lista_dicts:
                    horario = Horario.from_json(dic)
                    cls._DAO__objetos.append(horario)
        except (FileNotFoundError, json.JSONDecodeError):
            cls._DAO__objetos = []

    @classmethod
    def salvar(cls):
        with open("horarios.json", "w", encoding="utf-8") as arquivo:
            json.dump([h.to_json() for h in cls._DAO__objetos], arquivo, ensure_ascii=False, indent=4)
