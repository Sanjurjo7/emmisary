#!/usr/bin/env python
import pygame
import sys
from pygame.locals import *

WIDTH = 900
HEIGHT = 600
ACC = 0.5
FRIC = -0.12
FPS = 60
GRAVITY = 0.5

pygame.init()
vec = pygame.math.Vector2 # 2 for two dimensional

FramePerSec = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((32, 48))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect(center = (10, 420))

        self.pos = vec((110, 400))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.falling = True

    def move(self):
        self.acc = vec(0,GRAVITY)

        # This if statement removes air movement.
        if not self.falling:
            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[K_LEFT]:
                self.acc.x = -ACC
            if pressed_keys[K_RIGHT]:
                self.acc.x = ACC

            self.acc.x += self.vel.x * FRIC

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.falling = True
            self.vel.y = -12 - abs((self.vel.x)/2)

    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if P1.vel.y > 0:
            if hits:
                self.falling = False
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0
            print(self.acc.x)

class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

    def move(self):
        pass

PT1 = platform()
P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Emmisary")

def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    P1.jump()

        displaysurface.fill((0,0,0))
        P1.update()

        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
            entity.move()

        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__ == "__main__":
    main()
