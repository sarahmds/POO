import json
from datetime import datetime
from typing import List
from pathlib import Path
from .dao import DAO

BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_HORARIOS = BASE_DIR / "horarios.json"


class HorarioException(Exception):
    pass


class Horario:
    def __init__(self, id: int, data):
        self.set_id(id)
        self.set_data(data)
        self.set_confirmado(False)
        self.set_id_cliente(0)
        self.set_id_servico(0)
        self.set_id_profissional(0)
        self.profissional_nome = "—"

    # Getters e Setters -----------------
    def get_id(self): return self.__id
    def get_data(self): return self.__data
    def get_confirmado(self): return self.__confirmado
    def get_id_cliente(self): return self.__id_cliente
    def get_id_servico(self): return self.__id_servico
    def get_id_profissional(self): return self.__id_profissional

    def set_id(self, id): self.__id = id

    def set_data(self, data):
        """Aceita datetime ou string e converte corretamente."""
        if isinstance(data, str):
            try:
                data = datetime.strptime(data, "%d/%m/%Y %H:%M")
            except ValueError:
                raise HorarioException("Formato de data inválido. Use '%d/%m/%Y %H:%M'.")

        if not isinstance(data, datetime):
            raise HorarioException("Data deve ser um objeto datetime.")

        if data.year < 2020:
            raise HorarioException("Data inválida (anterior a 2020).")

        self.__data = data

    def set_confirmado(self, confirmado): self.__confirmado = bool(confirmado)
    def set_id_cliente(self, id_cliente): self.__id_cliente = id_cliente or 0
    def set_id_servico(self, id_servico): self.__id_servico = id_servico or 0
    def set_id_profissional(self, id_profissional): self.__id_profissional = id_profissional or 0

    # JSON -----------------
    def to_json(self):
        return {
            "id": self.__id,
            "data": self.__data.strftime("%d/%m/%Y %H:%M"),
            "confirmado": self.__confirmado,
            "id_cliente": self.__id_cliente,
            "id_servico": self.__id_servico,
            "id_profissional": self.__id_profissional,
            "profissional_nome": self.profissional_nome
        }

    @staticmethod
    def from_json(dic):
        """Cria objeto Horario a partir do dicionário JSON"""
        data_str = dic.get("data")
        data_obj = datetime.strptime(data_str, "%d/%m/%Y %H:%M") if data_str else datetime.now()
        h = Horario(dic.get("id", 0), data_obj)
        h.set_confirmado(dic.get("confirmado", False))
        h.set_id_cliente(dic.get("id_cliente", 0))
        h.set_id_servico(dic.get("id_servico", 0))
        h.set_id_profissional(dic.get("id_profissional", 0))
        h.profissional_nome = dic.get("profissional_nome", "—")
        return h

    def __str__(self):
        return f"{self.__id} - {self.__data.strftime('%d/%m/%Y %H:%M')} - {self.profissional_nome}"


class HorarioDAO(DAO):
    @classmethod
    def abrir(cls):
        cls._DAO__objetos = []
        try:
            with open(ARQUIVO_HORARIOS, "r", encoding="utf-8") as arq:
                lista = json.load(arq)
                for d in lista:
                    h = Horario.from_json(d)
                    cls._DAO__objetos.append(h)
        except (FileNotFoundError, json.JSONDecodeError):
            cls._DAO__objetos = []

    @classmethod
    def salvar(cls):
        with open(ARQUIVO_HORARIOS, "w", encoding="utf-8") as arq:
            json.dump([h.to_json() for h in cls._DAO__objetos],
                      arq, ensure_ascii=False, indent=4)
