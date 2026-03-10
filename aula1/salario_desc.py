v_hora = float(input("Digite o valor da hora de trabalho: "))
n_horas = float(input("Digite o numero de horas trabalhadas no mes: "))
    
    # Cálculos processados em sequencia
bruto = v_hora * n_horas
ir = bruto * 0.11
inss = bruto * 0.08
sind = bruto * 0.05
liquido = bruto - ir - inss - sind
    
    # Exibição dos resultados linha a linha
print(f"Salario Bruto: R$ {bruto:.2f}")
print(f"IR (11%): R$ {ir:.2f}")
print(f"INSS (8%): R$ {inss:.2f}")
print(f"Sindicato (5%): R$ {sind:.2f}")
print(f"Salario liquido: R$ {liquido:.2f}")