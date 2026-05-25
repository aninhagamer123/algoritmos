n = int(input("Digite um valor inteiro e positivo para n: "))

if n <= 0:
    print("O valor deve ser positivo!")
else:
    soma = 0

    # i = numero aleatorio
    # range = inicio e fim. se o numero digito for 5 ele vai ate +6 pela causa da pausa. 
    # ex: 10 seria do 1 ao 11. seria o intervalo. UM A MAIS.
    for i in range(1, n + 1):
        soma = soma + (1 / i)
        
    print(f"\nO resultado da soma S para n = {n} é: {soma:.1f}")