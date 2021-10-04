
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
            
            if int(passport["byr"]) not in range(1920,2002+1):
                print("flag1 (byr)", passport["byr"])
                continue
            elif int(passport["iyr"]) not in range(2010, 2020+1):
                print("flag2 (iyr)", passport["iyr"])
                continue
            elif int(passport["eyr"]) not in range(2020, 2030+1):
                print("flag3 (eyr)", passport["eyr"])
                continue
            elif len(passport["hcl"]) != 7 or passport["hcl"][0] != "#":
                print("flag4 (hcl)", passport["hcl"])
                continue
            elif passport["ecl"] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth", ]:
                print("flag5 (ecl)", passport["ecl"])
                continue
            elif len(passport["pid"]) != 9:
                print("flag6 (pid)", passport["pid"])
                continue
            
            if passport["hgt"][-2:] != "cm" and passport["hgt"][-2:] != "in":
                print("flag7 (hgt)", passport["hgt"])
                continue
            elif "cm" in passport["hgt"] and int(passport["hgt"].strip("cm")) not in range(150, 193+1):
                print("flag8 (hgt)", passport["hgt"])
                continue
            elif "in" in passport["hgt"] and int(passport["hgt"].strip("in")) not in range(58, 76+1):
                print("flag9 (hgt)", passport["hgt"])
                continue
                
            print("PASS")
            validPPs += 1


print(len(data))

print(validPPs)
