
primes = []

n = 1

flag = True

while len(primes) < 30:

	for i in range(2, n):
		
		if n % i == 0:
			flag = False
			break
	
		
	if flag:
		primes.append(n)
	
	
	flag = True
	n += 1

	
	
print(primes)
	
