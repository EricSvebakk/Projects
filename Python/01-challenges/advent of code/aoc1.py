
data = []

with open("data/aoc1_data.txt", "r") as myFile:

    for line in myFile:

        data.append(int(line.strip("\n")))

print(len(data))
#print(min(data))
index = 0
for i in data:
    for j in data:
        for l in data:
            index += 1
            
            if i + j + l == 2020:
                print(i, j, l, i * j * l)

print(index)