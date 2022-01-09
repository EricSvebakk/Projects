
from bs4 import BeautifulSoup
import pandas as pd


NAME = "../data/initialtesting/temp2"
FILENAME_KML = f"{NAME}.kml"
FILENAME_CSV = f"{NAME}.csv"


with open(FILENAME_KML) as data:
	soup = BeautifulSoup(data, "html.parser")

coordinates = soup.find_all("gx:coord")
time = soup.find_all("when")



rows = []

for i in range(len(time)):

	lon, lat, alt = coordinates[i].text.split(" ")
	
	year, month, day = time[i].text.split(':')[0].split("T")[0].split("-")
	
	
	rows.append([
		lon,
		lat,
		alt,
		f"{year}-{month}",
		year,
		month,
	])

df = pd.DataFrame(
	[*rows],
	columns=[
		"longitude",
		"latitude",
		"altitude",
		"time",
		"year",
		"month",
	]
)

df.to_csv(FILENAME_CSV, index=False)

print(df)
