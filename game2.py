import pygame
from pygame.locals import *

pygame.init()

screen_width = 1000
screen_height = 1000
tile_size = 50
game_over = 0;
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('GAME2')

#Загрузка фона
bg_img = pygame.image.load('sky.jpg')


class Player():
	def __init__(self, x, y):
		img = pygame.image.load('pygame_idle.png')
		self.image = pygame.transform.scale(img, (40, 80))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.widht = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.dead_image = pygame.image.load('flyDead.png')

	def update(self, game_over):
		dx = 0
		dy = 0

		if game_over == 0:
			#Настройка перемещения и прыжка
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False:
				self.vel_y = -15
				self.jumped = True
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 5
			if key[pygame.K_RIGHT]:
				dx += 5


			#Добавление грваитации
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			#Настройка столкновения
			for tile in world.tile_list:
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.widht, self.height):
					dx = 0

				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.widht, self.height):

					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0

			 #Настройка врагов
			if pygame.sprite.spritecollide(self, blocker_group, False):
				 game_over = -1

			 #Настройка лавы
			if pygame.sprite.spritecollide(self, lava_group, False):
				 game_over = -1

		#Координаты игрока
		self.rect.x += dx
		self.rect.y += dy

		if self.rect.bottom > screen_height:
			self.rect.bottom = screen_height
			dy = 0

		elif game_over == -1:
			self.image = self.dead_image
			if self.rect.y > 200:
				self.rect.y -= 5

		#Добавление игкора на экран
		screen.blit(self.image, self.rect)

		return game_over




class World():
	def __init__(self, data):
		self.tile_list = []

		dirt_img = pygame.image.load('box.png')
		grass_img = pygame.image.load('stone.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					blocker = Enemy(col_count * tile_size, row_count * tile_size + 15)
					blocker_group.add(blocker)
				if tile == 6:
					 lavas = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					 lava_group.add(lavas)
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('blockerMad.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move = 1
		self.movecounter = 0

	def update(self):
		self.rect.x += self.move
		self.movecounter += 1
		if abs(self.movecounter) > 50:
			self.move *= -1
			self.movecounter *= -1


class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		lava = pygame.image.load('liquidLavaTop.png')
		self.image = pygame.transform.scale(lava, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y



world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
[1, 0, 0, 0, 0, 2, 0, 0, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 2, 2, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]



player = Player(100, screen_height - 130)
blocker_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
world = World(world_data)

run = True
while run:

	screen.blit(bg_img, (0, 0))

	world.draw()

	if game_over == 0:
		blocker_group.update()

	blocker_group.draw(screen)
	lava_group.draw(screen)

	game_over = player.update(game_over)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
