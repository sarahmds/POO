def formatar_nome(nome):
    return nome.title()

nome = input("Digite seu nome: ")
print(f"Nome formatado: {formatar_nome(nome)}")