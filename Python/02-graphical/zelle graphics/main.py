

import graphics as g
import math
import pygame

screen = pygame.display.set_mode((500,500))

pygame.display.set_caption("heyo bitch")

image = pygame.image.load("image.png")
rect = image.get_rect()
image = pygame.transform.scale(image, rect.size)

ratio = round((rect.width/rect.height)*10)
print(ratio, round(ratio))

selectedObject = None
running = True
showkeys = False

distX = 0
distY = 0

while running:

    for event in pygame.event.get():

        # Allows closing window
        if event.type == pygame.QUIT:
            running = False

        # Allows moving objects
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            distX = rect.centerx - mouseX
            distY = rect.centery - mouseY
            selectedObject = rect
        elif event.type == pygame.MOUSEBUTTONUP:
            selectedObject = None

        # Defines actions for keypresses
        elif event.type == pygame.KEYDOWN:
            
            if showkeys:
                print(event.key)

            if event.key == pygame.K_q:
                running = False

            elif event.key == 45:
                print("POWERUP")
                rect.width += ratio * 10
                rect.height += 10 * 10
                image = pygame.transform.scale(image, rect.size)

            elif event.key == 47:
                print("POWERDOWN")
                rect.width -= ratio * 10
                rect.height -= 10 * 10
                image = pygame.transform.scale(image, rect.size)

            elif event.key == pygame.K_t:
                if showkeys:
                    showkeys = False
                else:
                    showkeys = True

            elif event.key == pygame.K_i:
                print(f"rs: {rect.size}")
                print(f"rr: {ratio}")
            
            print(event.key)

    # Moves selected object 
    if selectedObject:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        selectedObject.center = (mouseX+distX, mouseY+distY)

    screen.fill((255, 255, 255))
    screen.blit(image, rect)
    pygame.display.flip()

# im = Image.open("image.png")
# im.show("hey bitch")
# print(im.format, im.size, im.mode)

# x1, y1, x2, y2 = (0, 0, 50, 50)
# win = g.GraphWin("Graphics.py testing", width=600, height=600, autoflush=False)  # create a window
# win.setCoords(x1, y1, x2, y2)

# x = 0
# y = 0
# running = True
# while running:

#     key = win.checkKey()
#     # print(key)

#     if key == "q":
#         running = False
#         win.close()

#     elif key == "Right":
#         x += 1
#     elif key == "Left":
#         x -= 1
#     elif key == "Up":
#         y += 1
#     elif key == "Down":
#         y -= 1

#     square1 = g.Rectangle(g.Point(x1, y1), g.Point(x2, y2))
#     square1.setFill("white")
#     square1.draw(win)

#     square2 = g.Rectangle(g.Point(x+1, y+1), g.Point(x+9, y+9))
#     square2.draw(win)

#     # g.update(30)

