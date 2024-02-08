import pygame
#import neat
import time
import os
import random
import math
pygame.font.init()

WIN_WIDTH, WIN_HEIGHT = 600, 600
SHIPS =[pygame.image.load(os.path.join("src", "ship.png")), pygame.image.load(os.path.join("src", "ship2.png")), pygame.image.load(os.path.join("src", "ship3.png"))]
ASTEROID_B = pygame.image.load(os.path.join("src", "b.png"))
ASTEROID_M = pygame.transform.scale2x(pygame.image.load(os.path.join("src", "m.png")))
ASTEROID_S = pygame.transform.scale2x(pygame.image.load(os.path.join("src", "s.png")))
BG = pygame.transform.scale2x(pygame.image.load(os.path.join("src", "bg.png")))
STAT_FONT = pygame.font.SysFont("comicsans", 50)


class ship:
    def __init__(self):
        self.position = pygame.Vector2(WIN_WIDTH/2, WIN_HEIGHT/2)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.img = SHIPS[0]
        self.tilt = 0

    def move(self):
        self.acceleration = pygame.Vector2(math.sin(math.radians(self.tilt))*-1, math.cos(math.radians(self.tilt))*-1)
        self.position += self.velocity

        if self.position.x > WIN_WIDTH:
            self.position.x = -50
        if self.position.x+50 < 0:
            self.position.x = WIN_WIDTH
        if self.position.y > WIN_HEIGHT:
            self.position.y = -50
        if self.position.y+50 < 0:
            self.position.y = WIN_HEIGHT
    
    def tilter(self, axis):
        if axis == pygame.K_LEFT:
            self.tilt += 10
        if axis == pygame.K_RIGHT:
            self.tilt -= 10
        if self.tilt > 360:
            self.tilt = 1
        if self.tilt < 0:
            self.tilt = 359

    def draw(self, win):
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.position)).center)
        win.blit(rotated_image, new_rect.topleft)
                 
class asteroid:
    def __init__(self, size):
        if size == "B":
            self.x = random.randint(0, WIN_WIDTH)
            self.y = random.randint(0, WIN_HEIGHT)
            self.xa = random.randint(-5, 5)
            self.ya = random.randint(-5, 5)
            self.type = "B"
            self.tilt = 0
            self.img = ASTEROID_B
            self.width = 133
            self.height = 160

    def move(self):
        self.y += self.ya
        self.x += self.xa

        if self.x > WIN_WIDTH:
            self.x = self.width*-1
        if self.x+self.width < 0:
            self.x = WIN_WIDTH
        if self.y > WIN_HEIGHT:
            self.y = self.height*-1
        if self.y+self.height < 0:
            self.y = WIN_HEIGHT

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


class bullet:
    pass


def draw_window(win, rock, nave):
    win.blit(BG, (0,0))
    nave.draw(win)

    for asteroids in rock:
        asteroids.draw(win)


    pygame.display.update()


def main():
    run = True
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    rock = [asteroid("B"), asteroid("B"), asteroid("B"), asteroid("B"), asteroid("B")]
    nave = ship()

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.QUIT()
                    quit()                   
                
            if event.type == pygame.QUIT:
                run = False
                pygame.QUIT()
                quit()
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT]:
            nave.tilter(pygame.K_LEFT)
        if key_pressed[pygame.K_RIGHT]:
            nave.tilter(pygame.K_RIGHT)
        if key_pressed[pygame.K_UP]:
            nave.velocity += nave.acceleration
        if key_pressed[pygame.K_DOWN]:
            nave.velocity -= nave.acceleration

        for asteroids in rock:
            asteroids.move()
        if nave.velocity.x > 0 or nave.velocity.y > 0:
            nave.velocity -=pygame.Vector2(nave.velocity/20, nave.velocity/20)
        elif nave.velocity.x < 0 or nave.velocity.y < 0:
            nave.velocity -=pygame.Vector2(nave.velocity/20, nave.velocity/20)
        nave.move()
        draw_window(win, rock, nave)
        

if __name__ == "__main__":
    main()