soma = 0 
quantidade = 0

while True:
    try:
        numero = float(input("Digite um número (0 para sair): "))
        if numero == 0:
            break
        
        soma = soma + numero
        quantidade = quantidade + 1
        
    except ValueError:
        print("Entrada inválida. Digite um número.")

if quantidade > 0:
    print(f"\nResultados:")
    print(f"Quantidade de números: {quantidade}")
    print(f"Somatória: {soma}")
else:
    print("\nNenhum número foi digitado além do zero.")