
from sys import stdout

guess = 500
num = guess

response = ""

numguesses = 1
while numguesses <= 10:
	
	stdout.write(str(guess))
	stdout.flush()
	
	response = input()
	
	num //= 2
	
	if response.__eq__("higher"):
		guess += num
	elif response.__eq__("lower"):
		guess -= num
	elif response.__eq__("correct"):
		break
		
	numguesses += 1
