import math
base = float(input("Digite a base do retângulo: "))
altura = float(input("Digite a altura do retângulo: "))
area = base * altura
perimetro = 2 * (base + altura)
diagonal = math.sqrt(base*2 + altura*2)
print(f"Área = {area:.2f} - Perímetro = {perimetro:.2f} - Diagonal = {diagonal:.2f}")