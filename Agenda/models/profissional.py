from typing import Optional, Dict, Any, List

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
        return {"id": self.__id, "nome": self.__nome, "especialidade": self.__especialidade,
                "conselho": self.__conselho, "email": self.__email, "senha": self.__senha}

    @staticmethod
    def from_json(dic: Dict[str, Any]):
        return Profissional(dic["id"], dic["nome"], dic.get("especialidade", ""), dic.get("conselho", ""), dic.get("email", ""), dic.get("senha", ""))

    def __str__(self):
        return f"ID: {self.__id}, Nome: {self.__nome}, Especialidade: {self.__especialidade}, Conselho: {self.__conselho}, Email: {self.__email}"

class ProfissionalDAO:
    @staticmethod
    def inserir(p: Profissional):
        auth.profissional_inserir_raw(p.get_nome(), p.get_especialidade(), p.get_conselho(), p.get_email(), p.get_senha())

    @staticmethod
    def listar() -> List[Profissional]:
        return [Profissional.from_json(p) for p in auth.profissional_listar_raw()]

    @staticmethod
    def listar_id(id: int) -> Optional[Profissional]:
        raw_data = auth.profissional_listar_id_raw(id)
        return Profissional.from_json(raw_data) if raw_data else None

    @staticmethod
    def atualizar(p: Profissional) -> bool:
        return auth.profissional_atualizar_raw(p.get_id(), p.get_nome(), p.get_especialidade(), p.get_conselho(), p.get_email(), p.get_senha())

    @staticmethod
    def excluir(p: Profissional) -> bool:
        return auth.profissional_excluir_raw(p.get_id())

    @staticmethod
    def autenticar(email: str, senha: str) -> Optional[Dict[str, Any]]:
        return auth.profissional_autenticar(email, senha)
