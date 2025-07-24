class Cliente:
    def __init__(self, id, nome, email, fone):
        self.id = id
        self.nome = nome
        self.email = email
        self.fone = fone

    def __str__(self):
        return f"ID: {self.id}, Nome: {self.nome}, Email: {self.email}, Fone: {self.fone}"

    def get_id(self):
        return self.id

    def set_nome(self, nome):
        self.nome = nome

    def set_email(self, email):
        self.email = email

    def set_fone(self, fone):
        self.fone = fone


import json

class ClienteUI:
    objetos = []

    @staticmethod
    def main():
        while True:
            op = ClienteUI.menu()
            if op == 0:
                print("Saindo do programa.")
                break
            elif op == 1:
                ClienteUI.inserir()
            elif op == 2:
                ClienteUI.listar()
            elif op == 3:
                ClienteUI.listar_id()
            elif op == 4:
                ClienteUI.atualizar()
            elif op == 5:
                ClienteUI.excluir()
            elif op == 6:
                ClienteUI.abrir()
            elif op == 7:
                ClienteUI.salvar()
            else:
                print("Opção inválida!")

    @staticmethod
    def menu():
        print("\n--- Menu de Clientes ---")
        print("1 - Inserir novo cliente")
        print("2 - Listar todos os clientes")
        print("3 - Listar cliente por ID")
        print("4 - Atualizar cliente")
        print("5 - Excluir cliente")
        print("6 - Abrir clientes de arquivo")
        print("7 - Salvar clientes em arquivo")
        print("0 - Sair")
        return int(input("Escolha uma opção: "))

    @staticmethod
    def inserir():
        id = int(input("ID: "))
        nome = input("Nome: ")
        email = input("Email: ")
        fone = input("Fone: ")
        cliente = Cliente(id, nome, email, fone)
        ClienteUI.objetos.append(cliente)
        print("Cliente adicionado com sucesso.")

    @staticmethod
    def listar():
        for c in ClienteUI.objetos:
            print(c)

    @staticmethod
    def listar_id():
        id = int(input("Digite o ID do cliente: "))
        for c in ClienteUI.objetos:
            if c.get_id() == id:
                print(c)
                return
        print("Cliente não encontrado.")

    @staticmethod
    def atualizar():
        id = int(input("Digite o ID do cliente a ser atualizado: "))
        for c in ClienteUI.objetos:
            if c.get_id() == id:
                nome = input("Novo nome: ")
                email = input("Novo email: ")
                fone = input("Novo fone: ")
                c.set_nome(nome)
                c.set_email(email)
                c.set_fone(fone)
                print("Cliente atualizado.")
                return
        print("Cliente não encontrado.")

    @staticmethod
    def excluir():
        id = int(input("Digite o ID do cliente a ser removido: "))
        for i, c in enumerate(ClienteUI.objetos):
            if c.get_id() == id:
                del ClienteUI.objetos[i]
                print("Cliente removido.")
                return
        print("Cliente não encontrado.")

    @staticmethod
    def abrir():
        try:
            with open("clientes.json", "r") as arq:
                dados = json.load(arq)
                ClienteUI.objetos = [Cliente(**d) for d in dados]
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
                    {"id": c.id, "nome": c.nome, "email": c.email, "fone": c.fone}
                    for c in ClienteUI.objetos
                ]
                json.dump(dados, arq, indent=4)
                print("Clientes salvos em arquivo.")
        except Exception as e:
            print("Erro ao salvar arquivo:", e)
