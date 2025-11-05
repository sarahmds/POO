from typing import Optional, Dict, Any, List
import json
from .dao import DAO

class ProfissionalException(Exception):
    """Exceção para erros de validação de Profissional."""
    pass

class Profissional:
    def __init__(self, id: int, nome: str, especialidade: str, conselho: str, email: str, senha: str):
        if not nome.strip():
            raise ProfissionalException("Nome do profissional é obrigatório.")
        if not email.strip():
            raise ProfissionalException("Email do profissional é obrigatório.")
        if not senha.strip():
            raise ProfissionalException("Senha do profissional é obrigatória.")

        self.__id = id
        self.__nome = nome
        self.__especialidade = especialidade
        self.__conselho = conselho
        self.__email = email
        self.__senha = senha

    
    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_especialidade(self): return self.__especialidade
    def get_conselho(self): return self.__conselho
    def get_email(self): return self.__email
    def get_senha(self): return self.__senha

    def set_id(self, id: int):
        self.__id = id

    def set_nome(self, nome: str):
        if not nome.strip():
            raise ProfissionalException("Nome do profissional é obrigatório.")
        self.__nome = nome

    def set_especialidade(self, especialidade: str):
        self.__especialidade = especialidade

    def set_conselho(self, conselho: str):
        self.__conselho = conselho

    def set_email(self, email: str):
        if not email.strip():
            raise ProfissionalException("Email do profissional é obrigatório.")
        self.__email = email

    def set_senha(self, senha: str):
        if not senha.strip():
            raise ProfissionalException("Senha do profissional é obrigatória.")
        self.__senha = senha

    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.__id,
            "nome": self.__nome,
            "especialidade": self.__especialidade,
            "conselho": self.__conselho,
            "email": self.__email,
            "senha": self.__senha
        }

    @staticmethod
    def from_json(dic: Dict[str, Any]):
        return Profissional(
            dic["id"],
            dic.get("nome", ""),
            dic.get("especialidade", ""),
            dic.get("conselho", ""),
            dic.get("email", ""),
            dic.get("senha", "")
        )

    def __str__(self):
        return f"ID: {self.__id}, Nome: {self.__nome}, Especialidade: {self.__especialidade}, Conselho: {self.__conselho}, Email: {self.__email}"


class ProfissionalDAO(DAO):

    @classmethod
    def abrir(cls):
        cls._DAO__objetos = []
        try:
            with open("profissionais.json", "r", encoding="utf-8") as arquivo:
                lista_dicts = json.load(arquivo)
                from .profissional import Profissional
                for dic in lista_dicts:
                    profissional = Profissional.from_json(dic)
                    cls._DAO__objetos.append(profissional)
        except (FileNotFoundError, json.JSONDecodeError):
            cls._DAO__objetos = []

    @classmethod
    def salvar(cls):
        with open("profissionais.json", "w", encoding="utf-8") as arquivo:
            json.dump([p.to_json() for p in cls._DAO__objetos], arquivo, ensure_ascii=False, indent=4)

    @classmethod
    def autenticar(cls, email: str, senha: str) -> Optional[Dict[str, Any]]:
        """Autentica um profissional pelo email e senha."""
        cls.abrir()
        for prof in cls._DAO__objetos:
            if prof.get_email().lower() == email.lower() and prof.get_senha() == senha:
                return {
                    "id": prof.get_id(),
                    "nome": prof.get_nome(),
                    "email": prof.get_email(),
                    "especialidade": prof.get_especialidade(),
                    "conselho": prof.get_conselho()
                }
        return None
