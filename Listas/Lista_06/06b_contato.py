import json
from datetime import datetime

class Contato:
    def __init__(self, id, nome, email, fone, nascimento):
        self.id = id
        self.nome = nome
        self.email = email
        self.fone = fone
        self.nascimento = nascimento 

    def __str__(self):
        return f"ID: {self.id}, Nome: {self.nome}, Email: {self.email}, Fone: {self.fone}, Nascimento: {self.nascimento}"

    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome

    def get_email(self):
        return self.email

    def get_fone(self):
        return self.fone

    def get_nascimento(self):
        return self.nascimento

    def set_nome(self, nome):
        self.nome = nome

    def set_email(self, email):
        self.email = email

    def set_fone(self, fone):
        self.fone = fone

    def set_nascimento(self, nascimento):
        self.nascimento = nascimento


class ContatoUI:
    objetos = []

    @staticmethod
    def main():
        while True:
            op = ContatoUI.menu()
            if op == 0:
                print("Saindo do programa.")
                break
            elif op == 1:
                ContatoUI.inserir()
            elif op == 2:
                ContatoUI.listar()
            elif op == 3:
                ContatoUI.listar_id()
            elif op == 4:
                ContatoUI.atualizar()
            elif op == 5:
                ContatoUI.excluir()
            elif op == 6:
                ContatoUI.pesquisar()
            elif op == 7:
                ContatoUI.aniversariantes()
            elif op == 8:
                ContatoUI.abrir()
            elif op == 9:
                ContatoUI.salvar()
            else:
                print("Opção inválida!")

    @staticmethod
    def menu():
        print("\n--- Menu de contatos ---")
        print("1 - Inserir novo contato")
        print("2 - Listar todos os contatos")
        print("3 - Listar contato por ID")
        print("4 - Atualizar contato")
        print("5 - Excluir contato")
        print("6 - Pesquisar contato por iniciais do nome")
        print("7 - Listar aniversariantes do mês")
        print("8 - Abrir contatos de arquivo")
        print("9 - Salvar contatos em arquivo")
        print("0 - Sair")
        return int(input("Escolha uma opção: "))

    @staticmethod
    def inserir():
        id = int(input("ID: "))
        nome = input("Nome: ")
        email = input("Email: ")
        fone = input("Fone: ")
        nascimento = input("Nascimento (dd/mm/aaaa): ")
        contato = Contato(id, nome, email, fone, nascimento)
        ContatoUI.objetos.append(contato)
        print("Contato adicionado com sucesso.")

    @staticmethod
    def listar():
        for c in ContatoUI.objetos:
            print(c)

    @staticmethod
    def listar_id():
        id = int(input("Digite o ID do contato: "))
        for c in ContatoUI.objetos:
            if c.get_id() == id:
                print(c)
                return
        print("Cliente não encontrado.")

    @staticmethod
    def atualizar():
        id = int(input("Digite o ID do contato a ser atualizado: "))
        for c in ContatoUI.objetos:
            if c.get_id() == id:
                nome = input("Novo nome: ")
                email = input("Novo email: ")
                fone = input("Novo fone: ")
                nascimento = input("Nova data de nascimento (dd/mm/aaaa): ")
                c.set_nome(nome)
                c.set_email(email)
                c.set_fone(fone)
                c.set_nascimento(nascimento)
                print("Cliente atualizado.")
                return
        print("Cliente não encontrado.")

    @staticmethod
    def excluir():
        id = int(input("Digite o ID do cliente a ser removido: "))
        for i, c in enumerate(ContatoUI.objetos):
            if c.get_id() == id:
                del ContatoUI.objetos[i]
                print("Cliente removido.")
                return
        print("Cliente não encontrado.")

    @staticmethod
    def pesquisar():
        iniciais = input("Digite as iniciais do nome: ").lower()
        encontrados = [c for c in ContatoUI.objetos if c.get_nome().lower().startswith(iniciais)]
        if encontrados:
            for c in encontrados:
                print(c)
        else:
            print("Nenhum contato encontrado.")

    @staticmethod
    def aniversariantes():
        mes = input("Digite o número do mês (ex: 07): ")
        aniversariantes = []
        for c in ContatoUI.objetos:
            try:
                data = datetime.strptime(c.get_nascimento(), "%d/%m/%Y")
                if f"{data.month:02d}" == mes:
                    aniversariantes.append(c)
            except:
                pass
        if aniversariantes:
            for c in aniversariantes:
                print(c)
        else:
            print("Nenhum aniversariante encontrado nesse mês.")

    @staticmethod
    def abrir():
        try:
            with open("clientes.json", "r") as arq:
                dados = json.load(arq)
                ContatoUI.objetos = [Contato(**d) for d in dados]
                print("Clientes carregados do arquivo.")
        except FileNotFoundError:
            print("Arquivo não encontrado.")
        except Exception as e:
            print("Erro ao abrir arquivo:", e)

    @staticmethod
    def salvar():
        try:
            with open("clientes.json", "w") as arq:
                dados = [
                    {
                        "id": c.id,
                        "nome": c.nome,
                        "email": c.email,
                        "fone": c.fone,
                        "nascimento": c.nascimento
                    }
                    for c in ContatoUI.objetos
                ]
                json.dump(dados, arq, indent=4)
                print("Clientes salvos em arquivo.")
        except Exception as e:
            print("Erro ao salvar arquivo:", e)

if __name__ == "__main__":
    ContatoUI.main()
    