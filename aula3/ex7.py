distancia = float(input("Distância em km: "))

if distancia <= 200:
    preco = distancia * 0.50
else:
    preco = distancia * 0.45

print(f"Preço total da passagem: R$ {preco:.2f}")