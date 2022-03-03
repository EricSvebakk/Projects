
import pandas as pd
from pandas import DataFrame

df = pd.read_csv("title.basics.tsv", sep="\t")

print(df)

a = df["titleType"].unique()

print(a)

# Removes unnecessary columns
df = df.drop("tconst", 1)
df = df.drop("originalTitle", 1)
df = df.drop("endYear", 1)

# Removes unnecessary values from titleType
df = df.loc[df["titleType"].isin(["movie", "tvMovie"])]

# Converts tsv-NULL to 0
df = df.replace("\\N", 0)

# Converts column-values to integer
df["startYear"] = df["startYear"].astype(int)
df["runtimeMinutes"] = df["runtimeMinutes"].astype(int)

# Removes rows with startYear less than 1950
df = df.loc[df["startYear"] > 1975]
df = df.loc[df["startYear"] < 2023]
df = df.loc[df["runtimeMinutes"] > 0]


print(df)

df.to_csv("out.tsv", sep="\t", index=False)

