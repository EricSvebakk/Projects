
data = []

with open("jkb_day1_data.txt", "r") as myFile:

    for line in myFile:

        bits = line.split(",")
        data = bits

data.sort()

for i in range(100_000):
    
    if str(i) in data:
        continue
    
    print(i)

# for i in range(len(data)):
#     if data[i] + data[i+1] != data[i] * 2:
        