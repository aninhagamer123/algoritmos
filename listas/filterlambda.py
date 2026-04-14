lista1 = [1, 2, 3, 4, 5, 6]

filtra_impar_mais_um = filter(lambda x: x % 2 != 0, map(lambda x: x+1, lista1))
