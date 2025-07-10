class Pais:
    def __init__(self, id, nome, populacao, area):
        self.__id = id
        self.__nome = nome
        self.__populacao = populacao
        self.__area = area

    def get_id(self):
        return self.__id

    def get_nome(self):
        return self.__nome

    def set_nome(self, nome):
        self.__nome = nome

    def get_populacao(self):
        return self.__populacao

    def set_populacao(self, populacao):
        self.__populacao = populacao

    def get_area(self):
        return self.__area

    def set_area(self, area):
        self.__area = area

    def densidade(self):
        if self.__area == 0:
            return 0
        return self.__populacao / self.__area

    def __str__(self):
        return (f"ID: {self.__id} | Nome: {self.__nome} | População: {self.__populacao} | "
                f"Área: {self.__area} km² | Densidade: {self.densidade():.2f} hab/km²")

class PaisUI:
    __paises = []

    @classmethod
    def main(cls):
        op = 0
        while op != 7:
            op = cls.menu()
            if op == 1:
                cls.inserir()
            elif op == 2:
                cls.listar()
            elif op == 3:
                cls.atualizar()
            elif op == 4:
                cls.excluir()
            elif op == 5:
                cls.maispopuloso()
            elif op == 6:
                cls.maispovoado()
        print("Encerrando o cadastro.")

    @classmethod
    def menu(cls):
        print("\n1 - Inserir país")
        print("2 - Listar países")
        print("3 - Atualizar país")
        print("4 - Excluir país")
        print("5 - País mais populoso")
        print("6 - País mais povoado (densidade)")
        print("7 - Sair")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            print("Opção inválida!")
            return 0

    @classmethod
    def inserir(cls):
        try:
            id = int(input("ID: "))
            if any(p.get_id() == id for p in cls.__paises):
                print("ID já cadastrado!")
                return
            nome = input("Nome: ")
            populacao = int(input("População: "))
            area = float(input("Área (km²): "))
            p = Pais(id, nome, populacao, area)
            cls.__paises.append(p)
            print("País inserido com sucesso.")
        except ValueError:
            print("Dados inválidos.")

    @classmethod
    def listar(cls):
        if not cls.__paises:
            print("Nenhum país cadastrado.")
            return
        for p in cls.__paises:
            print(p)

    @classmethod
    def atualizar(cls):
        try:
            id = int(input("ID do país para atualizar: "))
            for p in cls.__paises:
                if p.get_id() == id:
                    nome = input(f"Novo nome ({p.get_nome()}): ")
                    if nome.strip():
                        p.set_nome(nome)
                    pop = input(f"Nova população ({p.get_populacao()}): ")
                    if pop.strip():
                        p.set_populacao(int(pop))
                    area = input(f"Nova área ({p.get_area()}): ")
                    if area.strip():
                        p.set_area(float(area))
                    print("País atualizado.")
                    return
            print("País não encontrado.")
        except ValueError:
            print("Entrada inválida.")

    @classmethod
    def excluir(cls):
        try:
            id = int(input("ID do país para excluir: "))
            for i, p in enumerate(cls.__paises):
                if p.get_id() == id:
                    del cls.__paises[i]
                    print("País excluído.")
                    return
            print("País não encontrado.")
        except ValueError:
            print("Entrada inválida.")

    @classmethod
    def maispopuloso(cls):
        if not cls.__paises:
            print("Nenhum país cadastrado.")
            return
        mais_pop = max(cls.__paises, key=lambda p: p.get_populacao())
        print("País mais populoso:")
        print(mais_pop)

    @classmethod
    def maispovoado(cls):
        if not cls.__paises:
            print("Nenhum país cadastrado.")
            return
        mais_dens = max(cls.__paises, key=lambda p: p.densidade())
        print("País com maior densidade demográfica:")
        print(mais_dens)


if __name__ == "__main__":
    PaisUI.main()