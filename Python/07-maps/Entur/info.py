
from pandas.core.frame import DataFrame
import pandas as pd

CODE = "RUT"

df1 = pd.read_csv(f"data/{CODE}/shapes.csv")
df2 = pd.read_csv(f"data/{CODE}/stops.csv")
df3 = pd.read_csv(f"data/{CODE}/trips.csv")
df4 = pd.read_csv(f"data/{CODE}/routes.csv")

print(df2["vehicle_type"].unique())

print(df4["route_type"].unique())


points = {
	"oslo S": [59.91109482593572, 10.75566383380521],
	"Jern B": [59.912268, 10.751326]
}

from math import sin, cos, atan2, sqrt, pi as PI

lat1, lon1 = points["oslo S"]
lat2, lon2 = points["Jern B"]

# Earths radius
R = 6371e3;

φ1 = lat1 * PI/180;
φ2 = lat2 * PI/180;
λ1 = lon1 * PI/180;
λ2 = lon2 * PI/180;
Δφ = (lat2-lat1) * PI/180;
Δλ = (lon2-lon1) * PI/180;

a = sin(Δφ/2) * sin(Δφ/2) + cos(φ1) * cos(φ2) * sin(Δλ/2) * sin(Δλ/2);
c = 2 * atan2(sqrt(a), sqrt(1-a));

d = R * c;

print(d)


x = (λ2-λ1) * cos((φ1+φ2)/2);
y = (φ2-φ1);
d = sqrt(x*x + y*y) * R;

print(d)