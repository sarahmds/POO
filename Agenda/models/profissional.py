from typing import Optional, Dict, Any, List

# Armazenamento em memória para simular banco de dados
profissionais_storage: List[Dict[str, Any]] = []

class Profissional:
    def __init__(self, id: int, nome: str, especialidade: str, conselho: str, email: str, senha: str):
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

    def set_nome(self, nome: str): self.__nome = nome
    def set_especialidade(self, especialidade: str): self.__especialidade = especialidade
    def set_conselho(self, conselho: str): self.__conselho = conselho
    def set_email(self, email: str): self.__email = email
    def set_senha(self, senha: str): self.__senha = senha

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
            dic["nome"],
            dic.get("especialidade", ""),
            dic.get("conselho", ""),
            dic.get("email", ""),
            dic.get("senha", "")
        )

    def __str__(self):
        return f"ID: {self.__id}, Nome: {self.__nome}, Especialidade: {self.__especialidade}, Conselho: {self.__conselho}, Email: {self.__email}"

class ProfissionalDAO:
    @staticmethod
    def inserir(p: Profissional):
        profissionais_storage.append(p.to_json())

    @staticmethod
    def listar() -> List[Profissional]:
        return [Profissional.from_json(p) for p in profissionais_storage]

    @staticmethod
    def listar_id(id: int) -> Optional[Profissional]:
        raw_data = next((p for p in profissionais_storage if p["id"] == id), None)
        return Profissional.from_json(raw_data) if raw_data else None

    @staticmethod
    def atualizar(p: Profissional) -> bool:
        raw_data = next((pr for pr in profissionais_storage if pr["id"] == p.get_id()), None)
        if raw_data:
            raw_data.update(p.to_json())
            return True
        return False

    @staticmethod
    def excluir(p: Profissional) -> bool:
        global profissionais_storage
        for i, pr in enumerate(profissionais_storage):
            if pr["id"] == p.get_id():
                profissionais_storage.pop(i)
                return True
        return False

    @staticmethod
    def autenticar(email: str, senha: str) -> Optional[Dict[str, Any]]:
        return next(
            (p for p in profissionais_storage if p["email"] == email and p["senha"] == senha),
            None
        )
