a = int(input("Digite o primeiro valor: "))
b = int(input("Digite o segundo valor: "))
c = int(input("Digite o terceiro valor: "))

print("Valores em ordem decrescente:")

if a > b and a > c:
    if b > c:
        print(a, b, c)
    else:
        print(a, c, b)
elif b > a and b > c:
    if a > c:
        print(b, a, c)
    else:
        print(b, c, a)
else: # Se o C for o maior
    if a > b:
        print(c, a, b)
    else:
        print(c, b, a)