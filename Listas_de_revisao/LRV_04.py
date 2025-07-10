class Viagem:
    """Modela uma viagem de carro."""

    def __init__(self, destino: str, distancia_km: float, combustivel_l: float):
        self.destino = destino              
        self.distancia_km = distancia_km    
        self.combustivel_l = combustivel_l  


    @property
    def destino(self):
        return self.__destino

    @destino.setter
    def destino(self, valor):
        if not valor or not valor.strip():
            raise ValueError("Destino não pode ser vazio.")
        self.__destino = valor.strip().title()

    @property
    def distancia_km(self):
        return self.__distancia_km

    @distancia_km.setter
    def distancia_km(self, valor):
        if valor <= 0:
            raise ValueError("Distância deve ser positiva.")
        self.__distancia_km = float(valor)

    @property
    def combustivel_l(self):
        return self.__combustivel_l

    @combustivel_l.setter
    def combustivel_l(self, valor):
        if valor <= 0:
            raise ValueError("Combustível deve ser positivo.")
        self.__combustivel_l = float(valor)

    def consumo(self) -> float:
        """Km por litro."""
        return self.distancia_km / self.combustivel_l

 
    def __str__(self):
        return (f"Viagem para {self.destino}: "
                f"{self.distancia_km:.1f} km, "
                f"{self.combustivel_l:.1f} L")


class ViagemUI:
    """Interface de linha de comando para Viagem."""

    @staticmethod
    def menu() -> int:
        print("\n=== Consumo médio de combustível ===")
        print("1 – Calcular")
        print("2 – Fim")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return 0

    @classmethod
    def calculo(cls):
        try:
            destino = input("Destino da viagem: ")
            distancia = float(input("Distância percorrida (km): "))
            litros = float(input("Combustível gasto (L): "))
            viagem = Viagem(destino, distancia, litros)   
        except ValueError as e:
            print("⚠️  Erro:", e)
            return

        print("\nDados da viagem:")
        print(" ", viagem)
        print(f"Consumo médio: {viagem.consumo():.2f} km/L")

    @classmethod
    def main(cls):
        while True:
            opc = cls.menu()
            if opc == 1:
                cls.calculo()
            elif opc == 2:
                break
            else:
                print("⚠️  Opção inválida.")




class Pais:
    """Modela dados básicos de um país."""

    def __init__(self, nome: str, populacao: int, area_km2: float):
        self.nome = nome            
        self.populacao = populacao  
        self.area_km2 = area_km2    


    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        if not valor or not valor.strip():
            raise ValueError("Nome não pode ser vazio.")
        self.__nome = valor.strip().title()

    @property
    def populacao(self):
        return self.__populacao

    @populacao.setter
    def populacao(self, valor):
        if valor <= 0:
            raise ValueError("População deve ser positiva.")
        self.__populacao = int(valor)

    @property
    def area_km2(self):
        return self.__area_km2

    @area_km2.setter
    def area_km2(self, valor):
        if valor <= 0:
            raise ValueError("Área deve ser positiva.")
        self.__area_km2 = float(valor)

  
    def densidade(self) -> float:
        """Habitantes por km²."""
        return self.populacao / self.area_km2

   
    def __str__(self):
        return (f"{self.nome}: {self.populacao:,} hab; "
                f"{self.area_km2:,.0f} km²".replace(",", "."))


class PaisUI:
    """Interface de linha de comando para País."""

    @staticmethod
    def menu() -> int:
        print("\n=== Densidade demográfica ===")
        print("1 – Calcular")
        print("2 – Fim")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return 0

    @classmethod
    def calculo(cls):
        try:
            nome = input("Nome do país: ")
            pop = int(input("População (habitantes): "))
            area = float(input("Área (km²): "))
            pais = Pais(nome, pop, area)   
        except ValueError as e:
            print("⚠️  Erro:", e)
            return

        print("\nDados do país:")
        print(" ", pais)
        print(f"Densidade demográfica: {pais.densidade():.2f} hab/km²")

    @classmethod
    def main(cls):
        while True:
            opc = cls.menu()
            if opc == 1:
                cls.calculo()
            elif opc == 2:
                break
            else:
                print("⚠️  Opção inválida.")


if __name__ == "__main__":
    ViagemUI.main()  
    PaisUI.main()    
    print("\nPrograma encerrado. Até mais!")
