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
C, N = map(int, input().split())
ponto_termino = C % N
print(ponto_termino)

# Beecrowd 1015 – Distância Entre Dois Pontos
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())
distancia = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
print(f"{distancia:.4f}")

# Beecrowd 1930 – Tomadas
T1, T2, T3, T4 = map(int, input().split())
tomadas_totais = T1 + T2 + T3 + T4
tomadas_totais -= 3
print(tomadas_totais)
