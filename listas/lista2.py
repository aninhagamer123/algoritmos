def starts_with_a(word):
    return word[0] == 'A'

lista=['Abacate', 'Abacaxi', 'Amora', 'Limão']
print(list(filter(starts_with_a, lista)))