#import libraries
import pygame
import math
import random
from tuts.enemy import Enemy
from tuts import button

#initialise pygame
pygame.init()

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Castle Defender')

clock = pygame.time.Clock()
FPS = 60

#define game variables
level = 1
high_score = 0
level_difficulty = 0
target_difficulty = 1000
DIFFICULTY_MULTIPLIER = 1.1
game_over = False
next_level = False
ENEMY_TIMER = 1000
last_enemy = pygame.time.get_ticks()
enemies_alive = 0


#define colours
WHITE = (255, 255, 255)
GREY = (100, 100, 100)

#define font
font = pygame.font.SysFont('Futura', 30)
font_60 = pygame.font.SysFont('Futura', 60)


#load images
bg = pygame.image.load('img/bg.png').convert_alpha()
#castle
castle_img_100 = pygame.image.load('img/castle/castle_100.png').convert_alpha()
castle_img_50 = pygame.image.load('img/castle/castle_50.png').convert_alpha()
castle_img_25 = pygame.image.load('img/castle/castle_25.png').convert_alpha()

#bullet image
bullet_img = pygame.image.load('img/bullet.png').convert_alpha()
b_w = bullet_img.get_width()
b_h = bullet_img.get_height()
bullet_img = pygame.transform.scale(bullet_img, (int(b_w * 0.075), int(b_h * 0.075)))

#load enemies
enemy_animations = []
enemy_types = ['knight', 'goblin', 'purple_goblin', 'red_goblin']
enemy_health = [75, 100, 125, 150]

animation_types = ['walk', 'attack', 'death']
for enemy in enemy_types:
	#load animation
	animation_list = []
	for animation in animation_types:
		#reset temporary list of images
		temp_list = []
		#define number of frames
		num_of_frames = 20
		for i in range(num_of_frames):
			img = pygame.image.load(f'img/enemies/{enemy}/{animation}/{i}.png').convert_alpha()
			e_w = img.get_width()
			e_h = img.get_height()
			img = pygame.transform.scale(img, (int(e_w * 0.2), int(e_h * 0.2)))
			temp_list.append(img)
		animation_list.append(temp_list)
	enemy_animations.append(animation_list)

#button images
#repair image
repair_img = pygame.image.load('img/repair.png').convert_alpha()
#armour image
armour_img = pygame.image.load('img/armour.png').convert_alpha()


#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


#function for displaying status
def show_info():
	draw_text('Money: ' + str(castle.money), font, GREY, 10, 10)
	draw_text('Score: ' + str(castle.score), font, GREY, 180, 10)
	draw_text('High Score: ' + str(high_score), font, GREY, 180, 30)
	draw_text('Level: ' + str(level), font, GREY, SCREEN_WIDTH // 2, 10)
	draw_text('Health: ' + str(castle.health) + " / " + str(castle.max_health), font, GREY, SCREEN_WIDTH - 230, SCREEN_HEIGHT - 50)
	draw_text('1000', font, GREY, SCREEN_WIDTH - 220 , 70)
	draw_text('500', font, GREY, SCREEN_WIDTH - 70 , 70)

#castle class
class Castle():
	def __init__(self, image100, image50, image25, x, y, scale):
		self.health = 1000
		self.max_health = self.health
		self.fired = False
		self.money = 5000
		self.score = 0

		width = image100.get_width()
		height = image100.get_height()

		self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
		self.image50 = pygame.transform.scale(image50, (int(width * scale), int(height * scale)))
		self.image25 = pygame.transform.scale(image25, (int(width * scale), int(height * scale)))
		self.rect = self.image100.get_rect()
		self.rect.x = x
		self.rect.y = y


	def shoot(self):
		pos = pygame.mouse.get_pos()
		x_dist = pos[0] - self.rect.midleft[0]
		y_dist = -(pos[1] - self.rect.midleft[1])
		self.angle = math.degrees(math.atan2(y_dist, x_dist))
		#get mouseclick
		if pygame.mouse.get_pressed()[0] and self.fired == False and pos[1] > 70:
			self.fired = True
			bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
			bullet_group.add(bullet)
		#reset mouseclick
		if pygame.mouse.get_pressed()[0] == False:
			self.fired = False



	def draw(self):
		#check which image to use based on health
		if self.health <= 250:
			self.image = self.image25
		elif self.health <= 500:
			self.image = self.image50
		else:
			self.image = self.image100

		screen.blit(self.image, self.rect)

	def repair(self):
		if self.money >= 1000 and self.health < self.max_health:
			self.health += 500
			self.money -= 1000
			if castle.health > castle.max_health:
				castle.health = castle.max_health

	def armour(self):
		if self.money >= 500:
			self.max_health += 250
			self.money -= 500


#bullet class
class Bullet(pygame.sprite.Sprite):
	def __init__(self, image, x, y, angle):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.angle = math.radians(angle)#convert input angle into radians
		self.speed = 10
		#calculate the horizontal and vertical speeds based on the angle
		self.dx = math.cos(self.angle) * self.speed
		self.dy = -(math.sin(self.angle) * self.speed)


	def update(self):
		#check if bullet has gone off the screen
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
			self.kill()			

		#move bullet
		self.rect.x += self.dx
		self.rect.y += self.dy



class Crosshair():
	def __init__(self, scale):
		image = pygame.image.load('img/crosshair.png').convert_alpha()
		width = image.get_width()
		height = image.get_height()

		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()

		#hide mouse
		pygame.mouse.set_visible(False)


	def draw(self):
		mx, my = pygame.mouse.get_pos()
		self.rect.center = (mx, my)
		screen.blit(self.image, self.rect)



#create castle
castle = Castle(castle_img_100, castle_img_50, castle_img_25, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 300, 0.2)

#create crosshair
crosshair = Crosshair(0.025)

#create buttons
repair_button = button.Button(SCREEN_WIDTH - 220, 10, repair_img, 0.5)
armour_button = button.Button(SCREEN_WIDTH - 75, 10, armour_img, 1.5)

#create groups
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


#game loop
run = True
while run:

	clock.tick(FPS)

	screen.blit(bg, (0, 0))

	#draw castle
	castle.draw()
	castle.shoot()

	#draw crosshair
	crosshair.draw()

	#draw bullets
	bullet_group.update()
	bullet_group.draw(screen)

	#draw enemies
	enemy_group.update(screen, castle, bullet_group)

	#show details
	show_info()

	#draw buttons
	if repair_button.draw(screen):
		castle.repair()
	if armour_button.draw(screen):
		castle.armour()

	#create enemies
	#check if max number of enemies has been reached
	if level_difficulty < target_difficulty:
		if pygame.time.get_ticks() - last_enemy > ENEMY_TIMER:
			#create enemies
			e = random.randint(0, len(enemy_types) -1)
			enemy = Enemy(enemy_health[e], enemy_animations[e], -100, SCREEN_HEIGHT - 100, 1)
			enemy_group.add(enemy)
			#reset enemy timer
			last_enemy = pygame.time.get_ticks()
			#incrase level difficulty by enemy health
			level_difficulty += enemy_health[e]


	#check if all the enemies have been spawned
	if level_difficulty >= target_difficulty:
		#check how many are still alive
		enemies_alive = 0
		for e in enemy_group:
			if e.alive == True:
				enemies_alive += 1
		#if there are none alive the level is complete
		if enemies_alive == 0 and next_level == False:
			next_level = True
			level_reset_time = pygame.time.get_ticks()

	#move onto the next level
	if next_level == True:
		draw_text('LEVEL COMPLETE!', font_60, WHITE, 200, 300)

		if pygame.time.get_ticks() - level_reset_time > 1500:
			next_level = False
			level += 1
			last_enemy = pygame.time.get_ticks()
			target_difficulty *= DIFFICULTY_MULTIPLIER
			level_difficulty = 0
			enemy_group.empty()




	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	#update display window
	pygame.display.update()

pygame.quit()