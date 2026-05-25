numeros = [x for x in range (1000)]
print(numeros)

arquivo_par = open('pares.txt', 'w')
arquivo_impar = open('impares.txt', 'w')

for x in numeros:
    if x % 2 == 0:
        arquivo_par.white(f'{x}\n')
    else:
        arquivo_impar.white(f'{x}\n')

arquivo_par.close()
arquivo_impar.close()