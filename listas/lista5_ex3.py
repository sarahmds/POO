def iniciais(nome):
    return ''.join([palavra[0].upper() for palavra in nome.split()])

nome = input("Digite seu nome completo: ")
print(f"Iniciais: {iniciais(nome)}")