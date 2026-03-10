while True:
    try:
        numero = float(input("Digite um numero entre 0 e 10: "))
        
        if 0 <= numero <= 10:
            print(f"Número válido: {numero}")
            break 
        else:
            print("Número fora do intervalo! Tente novamente.")
            
    except ValueError:
        print("Entrada inválida! Por favor, digite um número válido.")