
import requests
import re
from bs4 import BeautifulSoup


URL = "https://www.uio.no/studier/emner/matnat/ifi"
FILE_NAME = "uio_subjects"

SHOW_MSUB = True
SHOW_RSUB = True
SHOW_NREQ = False

REGEXPR_1 = "(?!IN1900)(IN[0-3]{1}[0-9]{3}[A-Z]?)"
REGEXPR_2 = REGEXPR_1

RELATE_TO = ""

try:
	open(FILE_NAME, 'w').close()
except FileNotFoundError:
	pass

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("td", {"class": "vrtx-course-description-name"})

num_results = 0

with open(FILE_NAME, "a") as file:

	for result in results:
		
		print("** ", end="")

		SUBJ = result.find("a")

		SUBJ_name = SUBJ.text.split(" ")[0]
		SUBJ_href = f"https://www.uio.no{SUBJ['href']}"

		SUBJ_page = requests.get(SUBJ_href)
		SUBJ_soup = BeautifulSoup(SUBJ_page.content, "html.parser")

		SUBJ_regEx = re.search(REGEXPR_1, SUBJ_name)

		
		if SUBJ_regEx:
			
			MSUB_soup = SUBJ_soup.find(text="Obligatoriske forkunnskaper")
			RSUB_soup = SUBJ_soup.find(text="Anbefalte forkunnskaper")

			MSUB_text = ""
			RSUB_text = ""
			
			
			if MSUB_soup != None and SHOW_MSUB:
				
				MSUB_subs = re.findall(REGEXPR_2, MSUB_soup.find_next().text)	
				
				for SUBJ in MSUB_subs:
					MSUB_text += f"  {SUBJ}"
			
			
			if RSUB_soup != None and SHOW_RSUB:
				
				RSUB_subs = re.findall(REGEXPR_2, RSUB_soup.find_next().text)
				
				for SUBJ in RSUB_subs:
					RSUB_text += f" *{SUBJ}"
			
			
			if (len(MSUB_text + RSUB_text) > 0):
				
				if RELATE_TO:
					
					text = f"{SUBJ_name}{MSUB_text}{RSUB_text}"
					
					if RELATE_TO in text:
						print(f"{SUBJ_name}{MSUB_text}{RSUB_text}", end="")
						file.write(f"{SUBJ_name}{MSUB_text}{RSUB_text}\n")
					
					# if RELATE_TO in 
					# if RELATE_TO in MSUB_text:
					# 	print(f"{SUBJ_name}  {RELATE_TO}", end="")
					# 	file.write(f"{SUBJ_name}  {RELATE_TO}\n")
						
					# elif RELATE_TO in RSUB_text:
					# 	print(f"{SUBJ_name} *{RELATE_TO}", end="")
					# 	file.write(f"{SUBJ_name} *{RELATE_TO}\n")
					
					
				else:
						
					print(f"{SUBJ_name}{MSUB_text}{RSUB_text}", end="")
					file.write(f"{SUBJ_name}{MSUB_text}{RSUB_text}\n")
				
				num_results += 1
				
				
			elif (SHOW_NREQ):
				print(f"{SUBJ_name}", end="")
				file.write(f"{SUBJ_name}\n")
				num_results += 1
		
		print()

print(f"# Results: {num_results}")
