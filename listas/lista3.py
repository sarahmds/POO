# Beecrowd 1004 – Produto Simples
a = int(input())
b = int(input())
print(f"PROD = {a * b}")

# Beecrowd 1005 – Média 1
a = float(input())
b = float(input())
media = ((a * 3.5) + (b * 7.5)) / 11
print(f"MEDIA = {media:.5f}")

# Beecrowd 1011 – Esfera
raio = float(input())
volume = (4/3) * 3.14159 * (raio**3)
print(f"VOLUME = {volume:.3f}")

# Beecrowd 2416 – Corrida
n1, n2 = map(int, input().split())
tempo = int(input())
velocidade = (n1 + n2) / tempo
print(f"{velocidade:.2f}")

# Beecrowd 1015 – Distância Entre Dois Pontos
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())
distancia = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
print(f"{distancia:.4f}")

# Beecrowd 1930 – Tomadas
n = int(input())
tomadas_totais = 0
for _ in range(n):
    tomadas = int(input())
    tomadas_totais += tomadas - 1
print(tomadas_totais)
