import pygame
from settings import *
from data_manager import *
from menu import Menu

# initialise pygame
pygame.init()
# initialise sound
pygame.mixer.init()

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jump Ball')

# # set frame rate
clock = pygame.time.Clock()

menu = Menu(screen)


# game loop
run = True
while run:

    clock.tick(FPS)

    menu.run()

    if menu.quit:
        run = False

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                
            run = False

    # update display window
    pygame.display.update()


pygame.quit()