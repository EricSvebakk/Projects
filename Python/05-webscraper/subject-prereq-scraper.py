
import requests
import re
from bs4 import BeautifulSoup

FILE_NAME = "sub-prereq-scrape"
CODE_LIMIT = 4000
NEED_PREQ = True
NEED_RREQ = True
ONLY_IN = True

# [A-Z]+(\-[A-Z]+)?[0-9]{4}\b

open(FILE_NAME, 'w').close()

URL = "https://www.uio.no/studier/emner/matnat/ifi/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all("td", {"class": "vrtx-course-description-name"})

with open(FILE_NAME, "a") as f:

	for r in results:

		result = r.find("a")

		result_name = result.text.split(" ")[0]
		result_href = f"https://www.uio.no{result['href']}"

		result_page = requests.get(result_href)

		result_soup = BeautifulSoup(result_page.content, "html.parser")

		result_pReq = result_soup.find(text="Obligatoriske forkunnskaper")
		result_rReq = result_soup.find(text="Anbefalte forkunnskaper")

		if result_name[:-4] == "IN" and (int(result_name[-4:]) < CODE_LIMIT):

			# 
			if ((result_pReq != None) or not NEED_PREQ) or ((result_rReq != None) or not NEED_RREQ):
				f.write(f"{result_name} ")
				print(f"{result_name} ", end="")

			# 
			if result_pReq != None and NEED_PREQ:

				result_sbjs = result_pReq.find_next('p').find_all('a')

				for subject in result_sbjs:
					subject_name = subject.text.split(' ')[0]

					if (subject_name[:-4] == "IN" and len(subject_name) == 6) or not ONLY_IN:
						f.write(f"{subject.text.split(' ')[0].strip()} ")
						print(f"{subject.text.split(' ')[0].strip()} ", end="")
			
			# 
			if result_rReq != None and NEED_RREQ:

				result_sbjs = result_rReq.find_next('p').find_all('a')

				for subject in result_sbjs:
					subject_name = subject.text.split(' ')[0]

					if (subject_name[:-4] == "IN" and len(subject_name) == 6) or not ONLY_IN:
						f.write(f"*{subject.text.split(' ')[0].strip()} ")
						print(f"*{subject.text.split(' ')[0].strip()} ", end="")
			
			# 
			if (result_pReq != None) or not NEED_PREQ:
				f.write("\n")
				print("")

		# elif result_name[:-4] == "IN" and (int(result_name[-4:]) >= CODE_LIMIT):
		# 	break
		
		
		# result_pReq = result_soup.find(text="Obligatoriske forkunnskaper")

		# result_name = result.text.split(" ")[0]
		
