lista1 = [x for x in range(1, 11)]
print(lista1)

lista2 = [x//2 for x in lista1 if x % 2 == 0]
print(lista2)