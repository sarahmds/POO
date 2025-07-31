from view.contato_view import ContatoView

class ContatoUI:
    @staticmethod
    def main():
        while True:
            op = ContatoUI.menu()
            if op == 0:
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

    @staticmethod
    def menu():
        print("\n1 - Inserir novo contato")
        print("2 - Listar todos os contatos")
        print("3 - Listar contato por ID")
        print("4 - Atualizar contato")
        print("5 - Excluir contato")
        print("0 - Sair")
        return int(input("Opção: "))

    @staticmethod
    def inserir():
        id = int(input("ID: "))
        nome = input("Nome: ")
        email = input("Email: ")
        fone = input("Fone: ")
        nascimento = input("Nascimento (dd/mm/aaaa): ")
        ContatoView.cliente_inserir(id, nome, email, fone, nascimento)
        print("Contato inserido.")

    @staticmethod
    def listar():
        contatos = ContatoView.cliente_listar()
        for c in contatos:
            print(c)

    @staticmethod
    def listar_id():
        id = int(input("ID: "))
        c = ContatoView.cliente_listar_id(id)
        print(c if c else "Contato não encontrado.")

    @staticmethod
    def atualizar():
        id = int(input("ID do contato a atualizar: "))
        nome = input("Novo nome: ")
        email = input("Novo email: ")
        fone = input("Novo fone: ")
        nascimento = input("Nova data de nascimento: ")
        ok = ContatoView.cliente_atualizar(id, nome, email, fone, nascimento)
        print("Atualizado." if ok else "Contato não encontrado.")

    @staticmethod
    def excluir():
        id = int(input("ID do contato a excluir: "))
        ok = ContatoView.cliente_excluir(id)
        print("Excluído." if ok else "Contato não encontrado.")
