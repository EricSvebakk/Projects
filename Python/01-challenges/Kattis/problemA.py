
numnums = int(input(""))

totnums = input().split(" ")
tot = 0

for i in range(numnums):
	tot += int(totnums[i])
	
print(tot)
