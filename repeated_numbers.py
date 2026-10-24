n = int(input("Введите n: "))

result = []
num = 1
while len(result) < n:
    result.extend([num] * num)
    num += 1

print(*result[:n], sep="")
