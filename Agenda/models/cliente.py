import auth
from typing import Optional, Dict, Any, List

class Cliente:
    def __init__(self, id: int, nome: str, email: str, fone: str, senha: str):
        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__fone = fone
        self.__senha = senha

    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_email(self): return self.__email
    def get_fone(self): return self.__fone
    def get_senha(self): return self.__senha

    def set_nome(self, nome: str): self.__nome = nome
    def set_email(self, email: str): self.__email = email
    def set_fone(self, fone: str): self.__fone = fone
    def set_senha(self, senha: str): self.__senha = senha

    def to_json(self) -> Dict[str, Any]:
        return {"id": self.__id, "nome": self.__nome, "email": self.__email, 
                "fone": self.__fone, "senha": self.__senha}

    @staticmethod
    def from_json(dic: Dict[str, Any]):
        return Cliente(dic["id"], dic["nome"], dic["email"], dic["fone"], dic.get("senha", ""))

    def __str__(self):
        return f"ID: {self.__id}, Nome: {self.__nome}, Email: {self.__email}, Fone: {self.__fone}"

class ClienteDAO:
    @staticmethod
    def inserir(c: Cliente):
        auth.cliente_inserir_raw(c.get_nome(), c.get_email(), c.get_fone(), c.get_senha())

    @staticmethod
    def listar() -> List[Cliente]:
        return [Cliente.from_json(c) for c in auth.cliente_listar_raw()]

    @staticmethod
    def listar_id(id: int) -> Optional[Cliente]:
        raw_data = auth.cliente_listar_id_raw(id)
        return Cliente.from_json(raw_data) if raw_data else None

    @staticmethod
    def atualizar(c: Cliente) -> bool:
        return auth.cliente_atualizar_raw(c.get_id(), c.get_nome(), c.get_email(), c.get_fone(), c.get_senha())

    @staticmethod
    def excluir(c: Cliente) -> bool:
        return auth.cliente_excluir_raw(c.get_id())

    @staticmethod
    def autenticar(email: str, senha: str) -> Optional[Dict[str, Any]]:
        """Autentica o cliente usando a função raw do módulo auth."""
        return auth.cliente_autenticar(email, senha)
