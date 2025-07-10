import datetime
import enum

class Paciente:
    def __init__(self, n: str, c: str, t: str, nasc: datetime.datetime):
        self._nome = n
        self._cpf = c
        self._telefone = t
        self._nascimento = nasc

    def Idade(self) -> str:
        hoje = datetime.datetime.today()
        anos = hoje.year - self._nascimento.year
        meses = hoje.month - self._nascimento.month
        if hoje.day < self._nascimento.day:
            meses -= 1
        if meses < 0:
            anos -= 1
            meses += 12
        return f"{anos} anos e {meses} meses"

    def ToString(self) -> str:
        return f"Nome: {self._nome}\nCPF: {self._cpf}\nTelefone: {self._telefone}\nNascimento: {self._nascimento}\nIdade: {self.Idade()}"
