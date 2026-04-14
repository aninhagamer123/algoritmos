def quadrado(num):
    return num*num

lista= [1,2,3,4]
lista_ao_quadrado = list (map(quadrado, lista))
print(lista_ao_quadrado)