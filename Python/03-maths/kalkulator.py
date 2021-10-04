
from os import system

pad = 10

# Exits programloop if base X is 0
while (baseX := input(f"{'Base X:':<{pad}}")) != "0":
    
    # Checks if both bases are integers
    try:
        baseX = int(baseX)
        baseY = int(input(f"{'Base Y:':<{pad}}"))
        
        # Number to be translated from base X to base Y
        num = input(f"{'Tall X:':<{pad}}")
        
        # Converts num from base X to base 10
        temp = int(num, baseX)
    
    # Prints an error-message if a base is not an integer
    # Resets terminal content and the user may try again
    except:
        system("cls")
        print("Try again. (The base must be an integer value)")
        continue
    
    # Converts num from base 10 to base Y
    num = ""
    while (temp != 0):
        (temp, rest) = divmod(temp, baseY)
        num = f"{rest}{num}"

    # End result
    print(f"{'Tall Y:':<{pad}}{num}")
    print(f"Set Base X as 0 to exit program\n")

