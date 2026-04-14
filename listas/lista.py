lista1 = ['a','b','c']
lista2 = [1, 2, 3]

lista1.extend(lista2)
lista3 = lista1.copy()
print(lista3)
lista4 = lista3 + lista1
print(lista4)