#cometario do calculo
from math import log

#ex2: calcular o valor do aluguel do carro
km = float(input("Digite a quantidade de quilômetros percorridos: "))
dias = int(input("Digite a quantidade de dias: "))
total = (dias * 60) + (km * 0.15)
print(f"Total a pagar: {total:.2f}")
#ou %2f % total                                                                                                                      