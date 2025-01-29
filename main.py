import pygame
pygame.init()

SCREEN_SIZE = (600, 600)

screen = pygame.display.set_mode(SCREEN_SIZE)

while True:

    events = pygame.event.get()

    for event in events:

        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)


    pygame.display.update()