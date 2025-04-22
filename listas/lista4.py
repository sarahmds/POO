# Beecrowd 1036 – Fórmula de Bhaskara
import math

a, b, c = map(float, input().split())

delta = b**2 - 4*a*c

if delta < 0 or a == 0:
    print("Impossivel calcular")
else:
    r1 = (-b + math.sqrt(delta)) / (2 * a)
    r2 = (-b - math.sqrt(delta)) / (2 * a)
    print(f"R1 = {r1:.5f}")
    print(f"R2 = {r2:.5f}")

# Beecrowd 1044 – Múltiplos
x, y = map(int, input().split())

if y % x == 0 or x % y == 0:
    print("Sao Multiplos")
else:
    print("Nao sao Multiplos")

# Beecrowd 1049 – Animal
codigo = int(input())

if codigo == 1:
    print("Verde")
elif codigo == 2:
    print("Amarelo")
elif codigo == 3:
    print("Azul")

# Beecrowd 1050 – DDD
codigo = int(input())

ddd_dict = {
    61: "Brasilia",
    71: "Salvador",
    11: "Sao Paulo",
    21: "Rio de Janeiro",
    32: "Juiz de Fora",
    19: "Campinas",
    27: "Vitoria",
    31: "Belo Horizonte"
}

print(ddd_dict.get(codigo, "DDD nao cadastrado"))

# Beecrowd 2424 – Tira-teima
x, y = map(int, input().split())

if x == y:
    print("O JOGO DUROU 24 HORA(S)")
elif x < y:
    print(f"O JOGO DUROU {y - x} HORA(S)")
else:
    print(f"O JOGO DUROU {24 - x + y} HORA(S)")

# Beecrowd 2670 – Máquina de Café
valores = list(map(int, input().split()))

if sum(valores) >= 50:
    print("S")
else:
    print("N")

# Beecrowd 1059 – Números Pares
for i in range(2, 101, 2):
    print(i)

# Beecrowd 1080 – Maior e Posição
numeros = [int(input()) for _ in range(5)]

maior = max(numeros)
posicao = numeros.index(maior) + 1

print(f"Maior valor: {maior}")
print(f"Posicao: {posicao}")

# Beecrowd 1094 – Experiências
n = int(input())

for _ in range(n):
    c, p = map(int, input().split())
    if p == 0:
        print("0")
    else:
        resultado = c / p
        print(f"{resultado:.4f}")

# Beecrowd 1114 – Senha Fixa
while True:
    senha = int(input())
    if senha == 2002:
        print("Acesso Permitido")
        break
    else:
        print("Senha Invalida")

# Beecrowd 1116 – Dividindo X por Y
while True:
    x, y = map(int, input().split())
    if y == 0:
        break
    print(f"{x / y:.1f}")

# Beecrowd 1151 – Fibonacci Fácil
n = int(input())
fib = [0, 1]
for i in range(2, n):
    fib.append(fib[i - 1] + fib[i - 2])

print(*fib[:n])
