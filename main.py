import pygame

from animation import Animation

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


def load_imgs_from_folder(path: str):

    imgs = []

    for i in range(20):
        img = pygame.image.load(f'./img/enemies/goblin/walk/{i}.png').convert_alpha()
        e_w = img.get_width()
        e_h = img.get_height()
        img = pygame.transform.scale(img, (int(e_w * 0.2), int(e_h * 0.2)))
        imgs.append(img)

    return imgs


class Goblin:

    def __init__(self, x, y):
        self.idle_animation = Animation(load_imgs_from_folder('path goes here'), True, .3)
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = 5.0
        self.current_animation = self.idle_animation

    def update(self, dt):
        self.current_animation.update(dt)

        self.rect.x += self.speed * dt / 100

    def draw(self, screen):
        screen.blit(self.current_animation.get_image(), self.rect)

castle = Castle(SCREEN_SIZE)

goblin = Goblin(100, 100)

clock = pygame.time.Clock()

while True:

    dt = clock.tick(60)

    goblin.update(dt)

    screen.blit(bg, (0, 0))
    castle.draw(screen)
    goblin.draw(screen)

    events = pygame.event.get()

    for event in events:

        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)


    pygame.display.update()