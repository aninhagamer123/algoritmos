from datetime import date

# Obtendo o ano atual dinamicamente
ano_atual = date.today().year

# Entrada de dados
ano_nascimento = int(input("Digite o seu ano de nascimento: "))

# Cálculo da idade
idade = ano_atual - ano_nascimento

print(f"\nVocê tem (ou fará) {idade} anos em {ano_atual}.")

# Verificação para Voto (16 anos ou mais)
if idade >= 16:
    print("Você já tem idade para votar!")
else:
    print(" Você ainda não tem idade para votar.")

# Verificação para CNH (18 anos ou mais)
if idade >= 18:
    print("Você já tem idade para tirar a Carteira de Habilitação!")
else:
    print(" Você ainda não tem idade para tirar a CNH.")