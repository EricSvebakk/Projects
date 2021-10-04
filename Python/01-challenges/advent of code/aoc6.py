
data = []

with open("data/aoc6_data.txt", "r") as myFile:

    group = []

    for line in myFile:

        line = line.strip()

        if line == "":
            if group:
                data.append(group)
                group = []
        else:
            group.append(line)

    if group:
        data.append(group)
        group = []

#print(data)

totSum = 0
for group in data:

    allQuestions = ""

    for person in group:
        for question in person:

            if question not in allQuestions:
                allQuestions += question

    totSum += len(allQuestions)

print(totSum)

totSum = 0
for group in data:

    allQuestions = "abcdefghijklmnopqrstuvwxyz"

    for person in group:
        for question in allQuestions:

            if question not in person:
                allQuestions = allQuestions.replace(question, "")

    totSum += len(allQuestions)

print(totSum)
