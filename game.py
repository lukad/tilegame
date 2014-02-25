#!/usr/bin/env python2
import pygame
import pygame.locals

from tiled import TileMap

FPS = 60
WIDTH = 640
HEIGHT = 480
SCALE = 1
SCALED_WIDTH = int(WIDTH * SCALE)
SCALED_HEIGHT = int(HEIGHT * SCALE)
RECT = (0, 0, SCALED_WIDTH, SCALED_HEIGHT)

def main():
	pygame.init()
	screen = pygame.display.set_mode((SCALED_WIDTH, SCALED_HEIGHT))
	backbuffer = pygame.Surface((WIDTH, HEIGHT))

	clock = pygame.time.Clock()

	tilemap = TileMap("level1.json")
	x, y = 0, 0

	running = True
	while running:
		tick = clock.tick(FPS)
		pygame.display.set_caption("Press Esc to quit. FPS: %.2f" % (clock.get_fps()))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_LEFT]:
			x += 2
		if pressed[pygame.K_RIGHT]:
			x -= 2
		if pressed[pygame.K_UP]:
			y += 2
		if pressed[pygame.K_DOWN]:
			y -= 2

		backbuffer.fill((0, 150, 255))
		tilemap.draw(backbuffer, x, y)
		screen.blit(pygame.transform.scale(backbuffer, (SCALED_WIDTH, SCALED_HEIGHT)), RECT)
		pygame.display.update()

if __name__ == "__main__":
	main()
