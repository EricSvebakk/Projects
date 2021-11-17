
N, Q = input().split(" ")

N = int(N)
Q = int(Q)


money = []
for i in range(N):
	money.append(0)


prints = []
for i in range(Q):
	
	event = input().split(" ")
	num = int(event[1])
	
	if event[0].__eq__("SET"):
		money[num - 1] = int(event[2])
	
	elif event[0].__eq__("RESTART"):
		for i in range(N):
			money[i] = num
	
	elif event[0].__eq__("PRINT"):
		prints.append(money[num - 1])

for i in prints:
	print(i)
