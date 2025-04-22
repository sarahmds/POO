def aprovado(nota1, nota2):
    media = (nota1 * 2 + nota2 * 3) / 5
    return media >= 60

n1 = int(input("Digite a nota do 1º bimestre: "))
n2 = int(input("Digite a nota do 2º bimestre: "))
print("Aprovado" if aprovado(n1, n2) else "Prova final")