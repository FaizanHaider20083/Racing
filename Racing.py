import pygame
import sys
import time
import random
from pygame.locals import *


fps = 60
framespersecond = pygame.time.Clock()
blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
black =(0,0,0)
white = (255,255,255)
speed = 5
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
score = 0

pygame.init()

font = pygame.font.SysFont("Verdana",60)
font_small = pygame.font.SysFont("Verdana",20)
game_over = font.render("Game Over",True,black)

ackground = pygame.image.load("AnimatedStreet.png")

displaysurface = pygame.display.set_mode((400,600))
displaysurface.fill(white)
pygame.display.set_caption("Temple Run on a budget")

class enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png")
        self.surf = pygame.Surface((50,80))
        self.rect = self.surf.get_rect(center = (random.randint(40,SCREEN_WIDTH-40),0))

    def move(self):
        global score
        self.rect.move_ip(0,speed)
        if (self.rect.bottom > 600):
            score += 1
            self.rect.top =0
            self.rect.center = (random.randint(30,370),0)

    


class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.surf = pygame.Surface((50,100))
        self.rect = self.surf.get_rect(center = (150,500))
        print("class initiated")

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5,0)
        
        if self.rect.right < 400:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5,0)

        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0,-5)

        if self.rect.bottom < 600:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,5)

    
class background():
    def __init__(self):
        self.bgimage = pygame.image.load('AnimatedStreet.png')
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0

        self.moving_speed = 5

    def update(self):
        self.bgY1 -= self.moving_speed
        self.bgY2 -= self.moving_speed
        if self.bgY1 <= -self.rectBGimg.height:
            self.bgY1 = self.rectBGimg.height
        if self.bgY2 <= -self.rectBGimg.height:
            self.bgY2 = self.rectBGimg.height

    def render(self):
        displaysurface.blit(self.bgimage,(self.bgX1,self.bgY1))
        displaysurface.blit(self.bgimage,(self.bgX2,self.bgY2))

    





Player = player()
Enemy = enemy()

enemies = pygame.sprite.Group()
enemies.add(Enemy)
all_sprites = pygame.sprite.Group()
all_sprites.add(Player)
all_sprites.add(Enemy)

increase_speed = pygame.USEREVENT + 1
pygame.time.set_timer(increase_speed,1000)

Background = background()


while True:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == increase_speed:
            speed += 2
    Background.update()
    Background.render()
    displaysurface.blit(ackground,(0,0))
    scores = font_small.render(str(score),True,black)
    displaysurface.blit(scores,(10,10))

    for entity in all_sprites:
       displaysurface.blit(entity.image,entity.rect)
       entity.move()

    if pygame.sprite.spritecollideany(Player,enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
        displaysurface.fill(red)
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()
    

    pygame.display.update()
    framespersecond.tick(fps)



