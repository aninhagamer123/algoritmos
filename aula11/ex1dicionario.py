def procuraChave(dict, value):
    lista = []
    for chave in dict.keys():
        if dict[chave] == value:
            lista.append(chave)
    return lista

def main():
    dict = {'alpha': 1, 'bravo': 2, 'charlie': 1,
            'delta': 3, 'echo': 1}
    
    value = int(input("Digite o valor a ser buscado:"))
    print(f"procurando chaves com valor {value}...")

    chaves_retornadas = procuraChave(dict, value)
    print(chaves_retornadas)

main()