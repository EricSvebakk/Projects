
data = []

with open("data/aoc2_data.txt", "r") as myFile:

    for line in myFile:

        bits = line.split()
        bits[1] = bits[1].strip(":")
        data.append(bits)

#print(data)


# part 1
# index = 0
# for bit in data:
#     bit[1] = bit[1].strip(":")
#     bitmin = int(bit[0].split("-")[0])
#     bitmax = int(bit[0].split("-")[1])

#     if bit[2].count(bit[1]) >= bitmin:
#         if bit[2].count(bit[1]) <= bitmax:
#             index += 1

# print(index)


# bit = data[7]
# chars = bit[0].split("-")

# print(bit)

# print(int(chars[0])-1, int(chars[1]))

# print(bit[2][int(chars[0])+1] == bit[1])
# print(bit[2][int(chars[1])+1] == bit[1])



# part 2
index = 0
for bit in data:
    char1 = int(bit[0].split("-")[0]) - 1
    char2 = int(bit[0].split("-")[1]) - 1

    try:
        if (bit[2][char1] == bit[1]) ^ (bit[2][char2] == bit[1]):
            index += 1

    except:
        continue

print(index)
