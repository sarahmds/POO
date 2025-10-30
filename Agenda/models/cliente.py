from typing import Optional, Dict, Any, List

clientes_storage: List[Dict[str, Any]] = []

class ClienteException(Exception):
    """Exceção personalizada para erros de Cliente."""
    pass

class Cliente:
    def __init__(self, id: int, nome: str, email: str, fone: str, senha: str):
        if not nome.strip():
            raise ClienteException("Nome do cliente é obrigatório.")
        if not email.strip():
            raise ClienteException("Email do cliente é obrigatório.")
        if not senha.strip():
            raise ClienteException("Senha do cliente é obrigatória.")

        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__fone = fone
        self.__senha = senha

    def get_id(self) -> int: return self.__id
    def get_nome(self) -> str: return self.__nome
    def get_email(self) -> str: return self.__email
    def get_fone(self) -> str: return self.__fone
    def get_senha(self) -> str: return self.__senha

    def set_nome(self, nome: str):
        if not nome.strip():
            raise ClienteException("Nome do cliente é obrigatório.")
        self.__nome = nome

    def set_email(self, email: str):
        if not email.strip():
            raise ClienteException("Email do cliente é obrigatório.")
        self.__email = email

    def set_fone(self, fone: str):
        self.__fone = fone

    def set_senha(self, senha: str):
        if not senha.strip():
            raise ClienteException("Senha do cliente é obrigatória.")
        self.__senha = senha

    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.__id,
            "nome": self.__nome,
            "email": self.__email,
            "fone": self.__fone,
            "senha": self.__senha
        }

    @staticmethod
    def from_json(dic: Dict[str, Any]):
        return Cliente(
            dic["id"],
            dic["nome"],
            dic["email"],
            dic.get("fone", ""),
            dic.get("senha", "")
        )

    def __str__(self):
        return f"ID: {self.__id}, Nome: {self.__nome}, Email: {self.__email}, Fone: {self.__fone}"


class ClienteDAO:
    """Classe DAO para manipulação de clientes em memória."""
    
    @staticmethod
    def inserir(c: Cliente):
        clientes_storage.append(c.to_json())

    @staticmethod
    def listar() -> List[Cliente]:
        return [Cliente.from_json(c) for c in clientes_storage]

    @staticmethod
    def listar_id(id: int) -> Optional[Cliente]:
        raw_data = next((c for c in clientes_storage if c["id"] == id), None)
        return Cliente.from_json(raw_data) if raw_data else None

    @staticmethod
    def atualizar(c: Cliente) -> bool:
        raw_data = next((cl for cl in clientes_storage if cl["id"] == c.get_id()), None)
        if raw_data:
            raw_data.update(c.to_json())
            return True
        return False

    @staticmethod
    def excluir(c: Cliente) -> bool:
        global clientes_storage
        for i, cl in enumerate(clientes_storage):
            if cl["id"] == c.get_id():
                clientes_storage.pop(i)
                return True
        return False

    @staticmethod
    def autenticar(email: str, senha: str) -> Optional[Dict[str, Any]]:
        return next((c for c in clientes_storage if c["email"] == email and c["senha"] == senha), None)
