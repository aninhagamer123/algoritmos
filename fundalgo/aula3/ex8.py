import math

altura = float(input("Altura do tanque: "))
raio = float(input("Raio do tanque: "))

# Cálculos Geométricos
area_base = math.pi * (raio ** 2)
perimetro = 2 * math.pi * raio
area_lateral = altura * perimetro
area_total = area_base + area_lateral

# Rendimento
litros_necessarios = area_total / 3.0
latas = math.ceil(litros_necessarios / 5.0)

# Estrutura de Precificação Aninhada
if latas == 1:
    preco_un = 50.00
else:
    if latas == 2:
        preco_un = 48.00
    else:
        if latas == 3:
            preco_un = 46.00
        else:
            preco_un = 45.00

custo_total = latas * preco_un

print(f"\nÁrea a ser pintada: {area_total:.2f}")
print(f"Qtde de litros: {litros_necessarios:.2f}")
print(f"Latas necessárias: {latas}")
print(f"Preço unitário: R$ {preco_un:.2f}")
print(f"Custo total: R$ {custo_total:.2f}")
