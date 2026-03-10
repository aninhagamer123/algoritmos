ano_atual = int(input("digite o ano atual: "))
ano_nasc = int(input("digite o seu ano de nascimento: "))
idade = ano_atual - ano_nasc

if idade > 18:
    print("oba, ja pode tirar sua CNH")

if idade < 18:
    print("nao pode tirar sua CNH")