import random

class Bingo:
    def __init__(self, numbolas):
        self.__numbolas = numbolas
        self.__bolas = set()
        self.__todas_bolas = set(range(1, numbolas + 1))

    def sortear(self):
        restantes = self.__todas_bolas - self.__bolas
        if not restantes:
            return -1
        bola = random.choice(list(restantes))
        self.__bolas.add(bola)
        return bola

    def sorteados(self):
        return sorted(self.__bolas)

class BingoUI:
    __bingo = None

    @classmethod
    def main(cls):
        op = 0
        while op != 4:
            op = cls.menu()
            if op == 1:
                cls.iniciarjogo()
            elif op == 2:
                cls.sortear()
            elif op == 3:
                cls.sorteados()
        print("Saindo do jogo. Até logo!")

    @classmethod
    def menu(cls):
        print("\n1 - Iniciar novo jogo")
        print("2 - Sortear número")
        print("3 - Ver números sorteados")
        print("4 - Sair")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            print("Opção inválida!")
            return 0

    @classmethod
    def iniciarjogo(cls):
        while True:
            try:
                num = int(input("Digite o número total de bolas: "))
                if num < 1:
                    print("Número deve ser maior que zero.")
                    continue
                cls.__bingo = Bingo(num)
                print(f"Novo jogo iniciado com {num} bolas.")
                break
            except ValueError:
                print("Digite um número válido.")

    @classmethod
    def sortear(cls):
        if cls.__bingo is None:
            print("Nenhum jogo iniciado. Inicie um jogo primeiro.")
            return
        bola = cls.__bingo.sortear()
        if bola == -1:
            print("Todas as bolas já foram sorteadas!")
        else:
            print(f"Bola sorteada: {bola}")

    @classmethod
    def sorteados(cls):
        if cls.__bingo is None:
            print("Nenhum jogo iniciado.")
            return
        print("Bolas sorteadas até agora:", cls.__bingo.sorteados())


if __name__ == "__main__":
    BingoUI.main()