x = int(input("Digite o valor que sera exibido a tabuada:"))

for i in range(1,11):
    
    print(f"{x} X {x} = {x * i}")

    #or

x = int(input("Digite o valor que sera exibido a tabuada:"))

for i in range(1,11):
    tab = x * i
    print("%d  X %d = %d" % (x,i, x*i)) 