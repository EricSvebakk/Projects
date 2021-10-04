

data = 5_433_000

primes = []

for possiblePrime in range(2, data):

    # Assume number is prime until shown it is not.
    isPrime = True
    for num in range(2, int(possiblePrime ** 0.5) + 1):
        if possiblePrime % num == 0:
            isPrime = False
            break

    if isPrime:
        primes.append(possiblePrime)

print(primes)

# for i in range(data):

#     closest = min(primes, key=lambda x: abs(x-i))
