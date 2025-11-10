import json
from typing import Optional, Dict, Any, List
from pathlib import Path


ARQUIVO_CLIENTES = Path("clientes.json")
def carregar_dados() -> List[Dict[str, Any]]:
    """Carrega os dados do arquivo JSON (se existir)."""
    if ARQUIVO_CLIENTES.exists():
        with open(ARQUIVO_CLIENTES, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []
def salvar_dados(dados: List[Dict[str, Any]]):
    """Salva os dados no arquivo JSON."""
    with open(ARQUIVO_CLIENTES, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
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

    def get_id(self) -> int:
        return self.__id

    def get_nome(self) -> str:
        return self.__nome

    def get_email(self) -> str:
        return self.__email

    def get_fone(self) -> str:
        return self.__fone

    def get_senha(self) -> str:
        return self.__senha
 
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
            "senha": self.__senha,
        }

    @staticmethod
    def from_json(dic: Dict[str, Any]) -> "Cliente":
        return Cliente(
            dic.get("id", 0),
            dic.get("nome", ""),
            dic.get("email", ""),
            dic.get("fone", ""),
            dic.get("senha", "")
        )

    def __str__(self):
        return f"ID: {self.__id}, Nome: {self.__nome}, Email: {self.__email}, Fone: {self.__fone}"

class ClienteDAO:
    """Classe DAO persistente em arquivo JSON."""

    @staticmethod
    def inserir(c: Cliente):
        dados = carregar_dados()
        novo_id = max((cli["id"] for cli in dados), default=0) + 1
        c_dict = c.to_json()
        c_dict["id"] = novo_id
        dados.append(c_dict)
        salvar_dados(dados)

    @staticmethod
    def listar() -> List[Cliente]:
        return [Cliente.from_json(c) for c in carregar_dados()]

    @staticmethod
    def listar_id(id: int) -> Optional[Cliente]:
        for c in carregar_dados():
            if c["id"] == id:
                return Cliente.from_json(c)
        return None

    @staticmethod
    def atualizar(c: Cliente) -> bool:
        dados = carregar_dados()
        for cli in dados:
            if cli["id"] == c.get_id():
                cli.update(c.to_json())
                salvar_dados(dados)
                return True
        return False

    @staticmethod
    def excluir(c: Cliente) -> bool:
        dados = carregar_dados()
        novos = [cli for cli in dados if cli["id"] != c.get_id()]
        if len(novos) != len(dados):
            salvar_dados(novos)
            return True
        return False

    @staticmethod
    def autenticar(email: str, senha: str) -> Optional[Dict[str, Any]]:
        for c in carregar_dados():
            if c["email"] == email and c["senha"] == senha:
                return c
        return None
