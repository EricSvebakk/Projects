
data = []

with open("data/aoc5_data.txt", "r") as myFile:

    passport = {}

    for line in myFile:

        line = line.strip()

        data.append(line)


data.sort(reverse=True)
allSeats = []
for boardingPass in data:

    allRows = [x for x in range(0, 128)]
    allCols = [x for x in range(0, 8)]
    chars = [boardingPass[:7], boardingPass[7:]]
    
    index = 0
    while len(allRows) > 1:

        if chars[0][index] == "F":
            middle = len(allRows)//2
            allRows = allRows[:middle]
        else:
            middle = len(allRows)//2
            allRows = allRows[middle:]
        index += 1
    else:
        row = allRows[0]

    index = 0
    while len(allCols) > 1:

        if chars[1][index] == "L":
            middle = len(allCols)//2
            allCols = allCols[:middle]
        else:
            middle = len(allCols)//2
            allCols = allCols[middle:]
        index += 1
    else:
        col = allCols[0]
    
    seatID = (row*8)+col
    allSeats.append(seatID)

print(max(allSeats))

for num in range(allSeats[0], allSeats[-1]):

    if num not in allSeats:
        print(num)