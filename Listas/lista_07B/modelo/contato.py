class Contato:
    def __init__(self, id, nome, email, fone, nascimento):
        self.id = id
        self.nome = nome
        self.email = email
        self.fone = fone
        self.nascimento = nascimento

    def __str__(self):
        return f"ID: {self.id}, Nome: {self.nome}, Email: {self.email}, Fone: {self.fone}, Nascimento: {self.nascimento}"

    def get_id(self): return self.id
    def get_nome(self): return self.nome
    def get_email(self): return self.email
    def get_fone(self): return self.fone
    def get_nascimento(self): return self.nascimento

    def set_nome(self, nome): self.nome = nome
    def set_email(self, email): self.email = email
    def set_fone(self, fone): self.fone = fone
    def set_nascimento(self, nascimento): self.nascimento = nascimento
