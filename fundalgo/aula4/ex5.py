codigo = int(input("Digite o código do produto: "))

# Classificação baseada na tabela
if codigo == 1:
    classificacao = "Alimento não perecível"
elif 2 <= codigo <= 4:
    classificacao = "Alimento perecível"
elif codigo == 5 or codigo == 6:
    classificacao = "Vestuário"
elif codigo == 7:
    classificacao = "Higiene pessoal"
elif 8 <= codigo <= 15:
    classificacao = "Limpeza e utensílios domésticos"
else:
    classificacao = "Inválido"

# Exibição do resultado
print(f"Classificação: {classificacao}")