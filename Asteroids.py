import pygame
#import neat
import time
import os
import random
import math
pygame.font.init()

WIN_WIDTH, WIN_HEIGHT = 1280, 900
BULLET  = pygame.image.load(os.path.join("src", "bullet.png"))
SHIPS =[pygame.image.load(os.path.join("src", "ship.png")), pygame.image.load(os.path.join("src", "ship2.png")), pygame.image.load(os.path.join("src", "ship3.png"))]
ASTEROID_B = pygame.image.load(os.path.join("src", "b.png"))
ASTEROID_M = pygame.image.load(os.path.join("src", "m.png"))
ASTEROID_S = pygame.image.load(os.path.join("src", "s.png"))
BG = pygame.transform.scale2x(pygame.image.load(os.path.join("src", "bg.png")))
STAT_FONT = pygame.font.SysFont("comicsans", 50)


class bullet:
    def __init__(self, position, acceleration,x,y):
        self.velocity = pygame.Vector2(x,y)
        self.position = pygame.Vector2(position.x+22, position.y+24)
        self.acceleration = acceleration
        self.img = BULLET

    def move(self):
        self.velocity += self.acceleration
        self.position += self.velocity

    def draw(self, win):
        win.blit(self.img, self.position)

    def get_mask(self):
        return pygame.mask.from_surface(self.img.convert_alpha())



class ship:
    SHIP = SHIPS
    ANIMATION = 3
    def __init__(self):
        self.position = pygame.Vector2(WIN_WIDTH/2, WIN_HEIGHT/2)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.img = SHIPS[0]
        self.tilt = 0
        self.img_count = 0

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

    def draw(self, win, fly):
        if fly:
            self.img_count +=1
            if self.img_count < self.ANIMATION:
                self.img = self.SHIP[0]
            elif self.img_count < self.ANIMATION+1:
                self.img = self.SHIP[1]
            elif self.img_count < self.ANIMATION+2:
                self.img = self.SHIP[2]
                self.img_count = 0
        else:
            if -5 <= self.velocity.x <= 5 and -5 <= self.velocity.y <= 5:
                self.img_count = 0
                self.img = self.SHIP[0]

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.position)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img.convert_alpha())
    
                 
class asteroid:
    def __init__(self, size, x, y):
        if size == "B":
            self.x = random.randint(0, WIN_WIDTH)
            self.y = random.randint(0, WIN_HEIGHT)
            self.xa = random.randint(-4, 4)
            self.ya = random.randint(-4, 4)
            self.type = "B"
            self.tilt = random.randint(0,359)
            self.img = ASTEROID_B
            self.width = 133
            self.height = 160
        if size == "M":
            self.x = x
            self.y = y
            self.xa = random.randint(-7, 7)
            self.ya = random.randint(-7, 7)
            self.type = "M"
            self.tilt = random.randint(0,359)
            self.img = ASTEROID_M
            self.width = 80
            self.height = 80
        if size == "S":
            self.x = x
            self.y = y
            self.xa = random.randint(-10, 10)
            self.ya = random.randint(-10, 10)
            self.type = "S"
            self.tilt = random.randint(0,359)
            self.img = ASTEROID_S
            self.width = 40
            self.height = 40

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
        aste = pygame.transform.rotate(self.img, self.tilt)
        win.blit(aste, (self.x, self.y))
    
    def collide(self, bullet = None, nave = None):

        if nave == None:
            asteroid_mask = pygame.mask.from_surface(self.img.convert_alpha())
            bullet_mask = bullet.get_mask()
            ba_offset = (self.x - bullet.position.x, self.y - round(bullet.position.y))
            ba_point = bullet_mask.overlap(asteroid_mask, ba_offset)
            if ba_point:return True

        else:
            asteroid_mask = pygame.mask.from_surface(self.img.convert_alpha())
            nave_mask = nave.get_mask()
            na_offset = (self.x - nave.position.x, self.y - round(nave.position.y))
            na_point = nave_mask.overlap(asteroid_mask, na_offset)
            if na_point: 
                return True
        
        return False    


def draw_window(win, rock, score, nav = None, bull = None, fly = False):
    win.blit(BG, (0,0))
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH -10 - text.get_width(), 5))
    for asteroids in rock:
        asteroids.draw(win)
    try:
        nav.draw(win, fly)
        for b in bull:
            b.draw(win)
    except:
        pass
    pygame.display.update()


def main():
    run = True
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    #rock = [asteroid("B"), asteroid("B"), asteroid("B"), asteroid("B"), asteroid("B")]
    rock = []
    nave = [ship()]
    shot = False
    bull =[]
    gigidy = 0

    while run:
        if len(nave) == 0:
            break
        if len(rock) == 0:
            for ast in range(5):
                rock.append(asteroid("B", 0, 0))
        if gigidy > 15:
            gigidy = 15
        if gigidy < 15:
            gigidy += 1
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
        for z, nav in enumerate(nave):
            if key_pressed[pygame.K_LEFT]:
                nav.tilter(pygame.K_LEFT)
            if key_pressed[pygame.K_RIGHT]:
                nav.tilter(pygame.K_RIGHT)
            if key_pressed[pygame.K_UP]:
                nav.velocity += nav.acceleration
                nav.draw(win, True)
            if key_pressed[pygame.K_DOWN]:
                nav.velocity -= nav.acceleration
            if key_pressed[pygame.K_SPACE] and gigidy == 15:
                bull.append(bullet(nav.position, nav.acceleration, nav.velocity.x, nav.velocity.y))
                shot = True
                gigidy = 0

        for y,aste in enumerate(rock):
            for z, nav in enumerate(nave):
                if aste.collide(False, nav):
                    print(f"Game over! Score: {score}")
                    nave.pop(z)
            for x, b in enumerate(bull):
                if aste.collide(b):
                    if aste.type == "B":
                        score += 20
                    elif aste.type == "M":
                        score += 50
                    elif aste.type == "S":
                        score += 100
                    bull.pop(x)
                    if aste.type == "B":
                        rock.append(asteroid("M", aste.x, aste.y))
                        rock.append(asteroid("M", aste.x, aste.y))
                    elif aste.type == "M":
                        rock.append(asteroid("S", aste.x, aste.y))
                        rock.append(asteroid("S", aste.x, aste.y))
                    rock.pop(y)


        for asteroids in rock:
            asteroids.move()
        if len(nave) > 0:
            for z, nav in enumerate(nave):
                if nav.velocity.x > 0 or nav.velocity.y > 0:
                    nav.velocity -=pygame.Vector2(nav.velocity/20, nav.velocity/20)
                elif nav.velocity.x < 0 or nav.velocity.y < 0:
                    nav.velocity -=pygame.Vector2(nav.velocity/20, nav.velocity/20)
                nav.move()
                if shot:
                    for x, b in enumerate(bull):
                        if (b.position.x < 0 or b.position.x > WIN_WIDTH)or(b.position.y < 0 or b.position.y > WIN_HEIGHT):
                            bull.pop(x)
                        b.move()
                    draw_window(win, rock, score, nav, bull)
                else:
                    draw_window(win, rock, score, nav)
        else:
            draw_window(win, rock, score)

if __name__ == "__main__":
    while True:
        main()