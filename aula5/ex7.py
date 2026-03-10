soma = 0        
contador = 1

print("Calculadora de Somatória")

while contador <= 10:
    numero = float(input(f"Digite o {contador}º número: "))
    
    soma = soma + numero  
    contador = contador + 1  

print(f"\nA soma total dos 10 números digitados é: {soma}")