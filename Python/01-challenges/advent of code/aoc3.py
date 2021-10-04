
data = []

with open("data/aoc3_data.txt", "r") as myFile:

    for line in myFile:

        data.append(line.strip())


steps = [(1,1),(3,1),(5,1),(7,1),(1,2)]

result2 = 1

for (steps1, steps2) in steps:

    result1 = 0

    index1 = 0
    index2 = 0

    for line in data:

        if index2 % steps2 != 0:
            index2 += 1
            continue
        

        if line[index1] == "#":
            result1 += 1

        index2 += 1

        index1 += steps1
        index1 %= len(line)

    print(result1)
    result2 *= result1

print(result2)
