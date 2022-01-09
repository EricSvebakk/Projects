
from pandas.core.frame import DataFrame
import pandas as pd

CODE = "RUT"

df1 = pd.read_csv(f"{CODE}/shapes.csv")
df2 = pd.read_csv(f"{CODE}/stops.csv")
df3 = pd.read_csv(f"{CODE}/trips.csv")
df4 = pd.read_csv(f"{CODE}/routes.csv")

print(df2["vehicle_type"].unique())

print(df4["route_type"].unique())