def maior(x, y):
    return x if x > y else y

a = int(input("Digite o primeiro número: "))
b = int(input("Digite o segundo número: "))
print(f"Maior valor: {maior(a, b)}")