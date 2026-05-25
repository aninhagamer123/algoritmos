preco = float(input("Digite o preço do produto: "))
codigo = int(input("Digite o código de origem: "))

# Lógica de classificação
if codigo == 1:
    procedencia = "Sul"
elif codigo == 2:
    procedencia = "Norte"
elif codigo == 3:
    procedencia = "Leste"
elif codigo == 4:
    procedencia = "Oeste"
elif codigo == 5 or codigo == 6:
    procedencia = "Nordeste"
elif 7 <= codigo <= 9:
    procedencia = "Sudeste"
elif 10 <= codigo <= 20:
    procedencia = "Centro-Oeste"
elif 25 <= codigo <= 30:
    procedencia = "Nordeste"
else:
    # Se não for nenhum dos códigos acima
    procedencia = "Importado"

# Saída dos resultados
print(f"\nO produto custa R$ {preco:.2f} e sua procedência é: {procedencia}")