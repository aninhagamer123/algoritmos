altura = float(input("Digite a altura (ex: 1.75): "))
sexo = input("Digite o sexo (M para masculino / F para feminino): ").strip().upper()

# Lógica de cálculo baseada no sexo
if sexo == 'M':
    peso_ideal = (72.7 * altura) - 58
    print(f"O peso ideal para um homem de {altura}m é: {peso_ideal:.2f} kg")
elif sexo == 'F':
    peso_ideal = (62.1 * altura) - 44.7
    print(f"O peso ideal para uma mulher de {altura}m é: {peso_ideal:.2f} kg")
else:
    print("Sexo inválido! Por favor, digite M ou F.")