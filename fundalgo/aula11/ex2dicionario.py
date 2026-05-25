import random

#dicionario vazio
contagem= {}

#gerar 100 numeros
for i in range(100):
    num = random.randint(0, 20) #sorteia o numero de 0 a 20

    #se o numero ja existe no dicionario adiciona mais 1
    if num in contagem:
        contagem[num] += 1 #soma mais uma vez para o numero
    else:
        contagem[num] = 1

#mostrar resultado
print("quantidade de vezes que o numero apareceu: \n")

for numero in contagem:
    print(f"{numero} apareceu {contagem[numero]} vezes")
