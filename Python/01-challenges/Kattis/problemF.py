
length = int(input())
text = input()

data = {
	"(": ")",
	"[": "]",
	"{": "}"
}

delimiters = []

for i in range(length):
		
	if (text[i].__eq__(" ")):
		continue
	
	elif text[i] in data.keys():
		delimiters.append(text[i])
		
	elif text[i] in data.values():
		flag = True
		
		if (len(delimiters) == 0):
			break
		
		for key in data.keys():
			
			if (len(delimiters) > 0):
				if delimiters[len(delimiters)-1] == key and text[i] == data[key]:
					delimiters.pop()
					flag = False
					break


if flag:
	print(text[i], i)
else:
	print("ok so far")
