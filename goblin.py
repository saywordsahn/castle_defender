import pygame
from animation import Animation

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
        self.speed = 10.0
        self.current_animation = self.idle_animation

    def update(self, dt):
        self.current_animation.update(dt)

        self.rect.x += self.speed * dt / 100

    def draw(self, screen):
        screen.blit(self.current_animation.get_image(), self.rect)