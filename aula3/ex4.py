salario = float(input("digite o valor do salario atual:"))

if salario > 1250.00:
    salario = salario * 1.1
    print("funcionario ganhou o direito de 10%")

else:
    salario = salario * 1.15
    print("novo salario é", salario)