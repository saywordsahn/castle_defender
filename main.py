import pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

screen = pygame.display.set_mode(SCREEN_SIZE)

bg = pygame.image.load('img/bg.png').convert_alpha()


class Castle:

    def __init__(self, SCREEN_SIZE):
        self.image = pygame.image.load('img/castle/castle_100.png')
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (width * .2, height * .2))
        self.x = SCREEN_SIZE[0] - 250
        self.y = SCREEN_SIZE[1] - 300



    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


castle = Castle(SCREEN_SIZE)

while True:

    screen.blit(bg, (0, 0))
    castle.draw(screen)

    events = pygame.event.get()

    for event in events:

        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)


    pygame.display.update()