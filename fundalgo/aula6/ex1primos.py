n = int(input("Digite n: "))

totalPrimos=0

for i in range(n):
     x = int(input("Digite x: "))
     if x > 1:
          primo = 1
          for j in range(2, x):
              if x % j == 0:
                 primo = 0
                 break   
              
          totalPrimos += primo
print(f"total primos = {totalPrimos}")