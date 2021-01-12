import pygame
import random
import time
import sys, os
import keyboard

pygame.init()
S_wight = 600
S_height = 600


def wall_1st(screen):
    image = pygame.image.load("brick.png")
    all_sprites = pygame.sprite.Group()
    x = 50
    y = 0
    for i in range(2):
        for j in range(47):
            brick = pygame.sprite.Sprite()
            brick.image = image
            brick.rect = brick.image.get_rect()
            all_sprites.add(brick)
            brick.rect.x = x
            brick.rect.y = y
            y = y + 13
        x = x - 27
        y = y - 15.4 * 40
    all_sprites.draw(screen)


def wall_2nd(screen):
    image = pygame.image.load("brick.png")
    all_sprites = pygame.sprite.Group()
    x = 523
    y = 0
    for i in range(2):
        for j in range(47):
            brick = pygame.sprite.Sprite()
            brick.image = image
            brick.rect = brick.image.get_rect()
            all_sprites.add(brick)
            brick.rect.x = x
            brick.rect.y = y
            y = y + 13
        x = x + 27
        y = y - 15.4 * 40
    all_sprites.draw(screen)

class Sounds:
    def __init__(self):
        self.bullet_sound = pygame.mixer.Sound("brrt.wav")
        self.bullet_sound.set_volume(0.2)
        self.lose = pygame.mixer.Sound("lose.wav")
        self.lose.set_volume(0.5)


class Player:
    def __init__(self, speed):
        self.image = pygame.image.load("jet.png")
        self.rect = self.image.get_rect(center = (300, 486))
        self.speed = speed
        self.bullets = pygame.sprite.Group()

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.x > 78:
            self.rect.x -= self.speed
        if key[pygame.K_RIGHT] and self.rect.x < S_wight - 135:
            self.rect.x += self.speed

    def draw(self, sc):
        sc.blit(self.image, self.rect)


class Bullet:
    def __init__(self, player):
        self.x = player.rect.x + 25.5
        self.y = player.rect.y
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.speed = 2
        self.bullets = []

    def draw(self, sc):
        sc.blit(self.image, (self.x, self.y))

    def perebor_and_move(self):
        for bullet in self.bullets:
            if bullet.y < S_height and bullet.y > 0:
                bullet.y -= bullet.speed
            else:
                self.bullets.pop(self.bullets.index(bullet))

    def control(self, player):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
             #pygame.time.delay(100)
             self.bullets.append(Bullet(player))


    def spawn(self, sc):
        for bullet in self.bullets:
            bullet.draw(sc)

    def check_colision(self, enemy):
        for bullet in self.bullets:
            if enemy.rect.colliderect(bullet):
                sys.exit()



class Enemy:
    def __init__(self, speed):
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect(center = (random.randint(80, 480), -10))
        self.speed = 2
        self.enemy_list = []
        self.enemies = pygame.USEREVENT
        pygame.time.set_timer(self.enemies, 550)

    def move(self):
        self.rect.y += self.speed


    def move1(self):
        for enemy in self.enemy_list:
            enemy.move()
            if self.rect.y > S_height:
                self.enemy_list.remove(enemy)

    def draw(self, sc):
        for enemy in self.enemy_list:
           sc.blit(self.image, enemy)

    def addEnemy(self):
        new_enemy = Enemy(self.speed)
        self.enemy_list.append(new_enemy)

    def check_colision(self, player, sound, sc):
        for enemy in self.enemy_list:
           if player.rect.colliderect(enemy):
               font = pygame.font.Font("20050.ttf", 36)
               text = font.render("You lose", True, (0,0,128), (0,255,0))
               text_rect = text.get_rect()
               text_rect.midbottom = (270, 500)
               sc.blit(text, text_rect)
               sound.lose.play()
               pygame.time.delay(5000)
               sys.exit()



def main():
    screen = pygame.display.set_mode((S_wight, S_height))
    pygame.display.set_caption("Літачок")
    jet = Player(3)
    enemy = Enemy(2)
    sound = Sounds()
    bulle = Bullet(jet)
    bg_image = pygame.image.load("sky.png")
    is_run = True
    #pygame.time.set_timer(pygame.USEREVENT + 1, 250)
    while is_run:
        screen.blit(bg_image, (0, 0))
        jet.draw(screen)
        jet.move()
        wall_1st(screen)
        wall_2nd(screen)
        enemy.draw(screen)
        enemy.move1()
        enemy.check_colision(jet, sound, screen)
        bulle.perebor_and_move()
        bulle.control(jet)
        bulle.spawn(screen)
        bulle.check_colision(enemy)
        for event in pygame.event.get():
            if event.type == enemy.enemies:
               enemy.addEnemy()
            if event.type == pygame.QUIT:
                is_run = False

        pygame.display.update()


if __name__ == "__main__":
    main()