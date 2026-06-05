import pygame
from screens.menu import Menu
from settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH

# initialise pygame
pygame.init()
# initialise sound
try:
    pygame.mixer.init()
except pygame.error as error:
    print(f"Could not initialize sound: {error}")

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

    # event handler
    for event in pygame.event.get():
        menu.handle_event(event)

        if event.type == pygame.QUIT:
            run = False

    menu.run()

    if menu.quit:
        run = False

    # update display window
    pygame.display.update()


pygame.quit()
