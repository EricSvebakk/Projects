
from os import system as sys

# +8 = 00001000
# -8 = 11111000

# +n = 0xxxxxxx
# -n = inverse(+n) + 1

def twos_comp(val, bits):

    mininum = -2**(bits-1)
    maximum = 2**(bits-1)-1

    if val >= mininum and val <= maximum:

        if val > 0:    
            val_b = f"{val:08b}"
        else:
            val_b = f"{(abs(abs(val) - (1 << bits))):b}"

        print(f"base 02: {val_b} \n")

    else:
        print(f"Not between {mininum} and {maximum} (Two's complement) \n")



while (inp := input("base 10: ")) != "0":
    try:
        twos_comp(int(inp), 8)
    except:
        pass

sys("cls")