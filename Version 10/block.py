import pygame
from settings import *

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        #self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill((0, 0, 255))

        self.image = pygame.image.load("block.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        screen.blit(self.image, self.rect) #Zeichnet das Spielerbild auf den Bildschirm (Position siehe oben self.rect)
    