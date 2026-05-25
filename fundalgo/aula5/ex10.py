total = 10
quant_alunos_aprovados = 0
soma_notas = 0 #contador
media_notas= 0 #acumulador

for i in range(0, total):
    nota = float(input())
    if nota >= 6.0:
       quant_alunos_aprovados += 1
       soma_notas += nota

    media_notas = soma_notas / total
    print(f"alunos_aprovados = {quant_alunos_aprovados}")
    print(f"media das notas = {media_notas:.1f}")
