
data = []

with open("data/aoc4_data.txt", "r") as myFile:

    passport = {}

    for line in myFile:
        
        line = line.strip()

        if line == "":
            if passport:
                data.append(passport)
                passport = {}

        else:
            bits = line.split()

            for bit in bits:
                key, val = bit.split(":")
                passport[key] = val

    if passport:
        data.append(passport)
        passport = {}


validPPs = 0

for passport in data:
    keys = passport.keys()
    #print(list(keys))

    # if len(keys) >= 7:
    #     if len(keys) == 8 or "cid" not in keys:
    #         validPPs += 1
    # if "pid" in keys:
    #     print(passport["pid"])
    # continue

    if len(keys) >= 7 :
        if len(keys) == 8 or "cid" not in keys:

            # print("flag1 (byr)", passport["byr"])
            # print("flag2 (iyr)", passport["iyr"])
            # print("flag3 (eyr)", passport["eyr"])
            # print("flag4 (hcl)", passport["hcl"])
            # print("flag5 (ecl)", passport["ecl"])
            # print("flag6 (pid)", passport["pid"])
            # print("flag7 (hgt)", passport["hgt"])
            # print("flag8 (hgt)", passport["hgt"])
            # print("flag9 (hgt)", passport["hgt"])
            correct = 0
            incorrect = {}

            if int(passport["byr"]) in range(1920,2002+1):
                correct += 1
            else:
                incorrect["byr"] = passport["byr"]

            if int(passport["iyr"]) in range(2010, 2020+1):
                correct += 1
            else:
                incorrect["iyr"] = passport["iyr"]

            if int(passport["eyr"]) in range(2020, 2030+1):
                correct += 1
            else:
                incorrect["eyr"] = passport["eyr"]

            if len(passport["hcl"]) == 7 and passport["hcl"][0] == "#":
                correct += 1
            else:
                incorrect["hcl"] = passport["hcl"]

            if passport["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth", ]:
                correct += 1
            else:
                incorrect["ecl"] = passport["ecl"]

            if len(passport["pid"]) == 9:
                correct += 1
            else:
                incorrect["pid"] = passport["pid"]
            
            if "cm" in passport["hgt"] and int(passport["hgt"].strip("cm")) in range(150, 193+1):
                correct += 1
            elif "in" in passport["hgt"] and int(passport["hgt"].strip("in")) in range(58, 76+1):
                correct += 1
            else:
                incorrect["hgt"] = passport["hgt"]
                
            if correct == 7:
                validPPs += 1
            else:
                print(correct, incorrect)
            


print(validPPs, "/", len(data))
