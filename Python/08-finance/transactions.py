
BRUKSKONTO = "42024804563"
FINANSKONTO = "42125368020"

REBECKA = "94890645636"
TL = "12082376095"

KONTO = "15064463877"

with open("OversiktKonti-01.01.2021-25.12.2021.csv","r") as yeet:
	
	updated = False
	text = ""
	
	dateCURRENT = ""
	priceCURRENT = 0
	priceTOTAL = 0
	
	for i in yeet:
		
		i = i.replace('"','').replace("\n","").split(";")
		
		# DATE
		if (dateCURRENT != i[0]):
			
			if (text != ""):
				print("\n", "-"*5, f"{dateCURRENT}", "-"*45)
				print(text)
			
			dateCURRENT = i[0]
			text = ""
			
		
		# VALID ACCOUNT
		if (i[5] == KONTO or i[6] == KONTO):
			
			# ACCOUNT NAME
			# if (i[5] == KONTO):
			# 	i[5] = "-"
			# elif (i[6] == KONTO):
			# 	i[6] = "-"
		
			# PRICE
			if (len(i[3]) > 0):
				priceCURRENT = i[3]
			elif (len(i[4]) > 0):
				priceCURRENT = i[4]
			
			priceCURRENT = float(priceCURRENT.replace(',', '.'))
			priceTOTAL += priceCURRENT
		
			# TEXT
			text += f"{i[1][:20]:<25}"
			temp = f"{priceCURRENT:.2f}"
			temp = f"{temp:>8}"
			temp = f"{temp:<12}"
			text += temp
			# text += f"{i[5]:<15}" + f"{i[6]:<15}"
			text += "|\n"
		
	print(f"\n\nTOTAL: {priceTOTAL :.2f}kr\n")


# with open("OversiktKonti-01.01.2021-25.12.2021.csv", "r") as yeet:
# 	mySet = {}
# 	for i in yeet:
		
# 		i = i.replace('"','').replace("\n","").split(";")
		
# 		# print(i)
		
# 		account = ""
# 		if (len(i[3]) == 0):
# 			account = i[5]
# 		elif (len(i[4]) == 0):
# 			account = i[6]
		
# 		# mySet.
# 		mySet[account] = i[1]
		
# 	print(mySet)
		
# 	with open("temp.csv","w") as yuck:
		
# 		for i in mySet.keys():
			
# 			yuck.write(f"{i},{mySet[i]}\n")
