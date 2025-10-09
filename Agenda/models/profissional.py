import json

class Profissional:
    def __init__(self, id, nome, profissao, email="", senha=""):
        self.set_id(id)
        self.set_nome(nome)
        self.set_profissao(profissao)
        self.set_email(email)
        self.set_senha(senha)

    # ---------- GETTERS ----------
    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_profissao(self): return self.__profissao
    def get_email(self): return self.__email
    def get_senha(self): return self.__senha

    # ---------- SETTERS ----------
    def set_id(self, id): self.__id = id
    def set_nome(self, nome): self.__nome = nome
    def set_profissao(self, profissao): self.__profissao = profissao
    def set_email(self, email): self.__email = email
    def set_senha(self, senha): self.__senha = senha

    # ---------- SERIALIZAÇÃO JSON ----------
    def to_json(self):
        return {
            "id": self.__id,
            "nome": self.__nome,
            "profissao": self.__profissao,
            "email": self.__email,
            "senha": self.__senha
        }

    @staticmethod
    def from_json(dic):
        return Profissional(
            dic["id"],
            dic["nome"],
            dic["profissao"],
            dic.get("email", ""),
            dic.get("senha", "")
        )

    def __str__(self):
        return f"{self.__id} - {self.__nome} - {self.__profissao} - {self.__email}"


# ---------- DAO ----------
class ProfissionalDAO:
    __objetos = []

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        novo_id = max([p.get_id() for p in cls.__objetos], default=0) + 1
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
        cls.__objetos = [p for p in cls.__objetos if p.get_id() != obj.get_id()]
        cls.salvar()

    @classmethod
    def abrir(cls):
        cls.__objetos = []
        try:
            with open("profissionais.json", "r", encoding="utf-8") as arquivo:
                lista_dicts = json.load(arquivo)
                for dic in lista_dicts:
                    prof = Profissional.from_json(dic)
                    cls.__objetos.append(prof)
        except (FileNotFoundError, json.JSONDecodeError):
            cls.__objetos = []

    @classmethod
    def salvar(cls):
        with open("profissionais.json", "w", encoding="utf-8") as arquivo:
            json.dump([Profissional.to_json(p) for p in cls.__objetos], arquivo, ensure_ascii=False, indent=4)
