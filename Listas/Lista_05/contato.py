import datetime
import enum

class Contato:
    def __init__(self, i: int, n: str, e: str, f: str, d: datetime.datetime):
        self._id = i
        self._nome = n
        self._email = e
        self._fone = f
        self._nascimento = d

    def ToString(self) -> str:
        return (
            f"ID: {self._id}\nNome: {self._nome}\nEmail: {self._email}\nFone: {self._fone}\nNascimento: {self._nascimento.strftime('%d/%m/%Y')}"
        )


class ContatoUI:
    contatos = []

    @staticmethod
    def Main():
        while True:
            opcao = ContatoUI.Menu()
            if opcao == 1:
                ContatoUI.Inserir()
            elif opcao == 2:
                ContatoUI.Listar()
            elif opcao == 3:
                ContatoUI.Atualizar()
            elif opcao == 4:
                ContatoUI.Excluir()
            elif opcao == 5:
                ContatoUI.Pesquisar()
            elif opcao == 6:
                ContatoUI.Aniversariantes()
            elif opcao == 0:
                break

    @staticmethod
    def Menu() -> int:
        print("\nAGENDA DE CONTATOS")
        print("1 - Inserir")
        print("2 - Listar")
        print("3 - Atualizar")
        print("4 - Excluir")
        print("5 - Pesquisar")
        print("6 - Aniversariantes")
        print("0 - Sair")
        try:
            return int(input("Escolha: "))
        except ValueError:
            return -1

    @staticmethod
    def Inserir():
        try:
            i = len(ContatoUI.contatos) + 1
            n = input("Nome: ")
            e = input("Email: ")
            f = input("Fone: ")
            d = datetime.datetime.strptime(input("Nascimento (dd/mm/aaaa): "), "%d/%m/%Y")
            ContatoUI.contatos.append(Contato(i, n, e, f, d))
            print("Contato adicionado!")
        except Exception as ex:
            print("Erro ao adicionar contato:", ex)

    @staticmethod
    def Listar():
        for c in ContatoUI.contatos:
            print("\n" + c.ToString())

    @staticmethod
    def Atualizar():
        try:
            id_alvo = int(input("ID do contato: "))
            for c in ContatoUI.contatos:
                if c._id == id_alvo:
                    n = input("Novo nome: ")
                    e = input("Novo email: ")
                    f = input("Novo fone: ")
                    d = datetime.datetime.strptime(input("Nova data de nascimento (dd/mm/aaaa): "), "%d/%m/%Y")
                    c._nome, c._email, c._fone, c._nascimento = n, e, f, d
                    print("Contato atualizado!")
                    return
            print("Contato não encontrado.")
        except Exception as ex:
            print("Erro:", ex)

    @staticmethod
    def Excluir():
        try:
            id_alvo = int(input("ID do contato: "))
            ContatoUI.contatos = [c for c in ContatoUI.contatos if c._id != id_alvo]
            print("Contato removido.")
        except:
            print("Erro ao remover.")

    @staticmethod
    def Pesquisar():
        iniciais = input("Digite as iniciais do nome: ").lower()
        encontrados = [c for c in ContatoUI.contatos if c._nome.lower().startswith(iniciais)]
        for c in encontrados:
            print("\n" + c.ToString())
        if not encontrados:
            print("Nenhum contato encontrado.")

    @staticmethod
    def Aniversariantes():
        try:
            mes = int(input("Digite o número do mês: "))
            encontrados = [c for c in ContatoUI.contatos if c._nascimento.month == mes]
            for c in encontrados:
                print("\n" + c.ToString())
            if not encontrados:
                print("Nenhum aniversariante neste mês.")
        except:
            print("Mês inválido.")

