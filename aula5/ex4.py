maior = 0

for i in range(0,6):
    valor = int(input())
    if valor > maior:
        maior = valor
print(f"MAIOR = {maior}")