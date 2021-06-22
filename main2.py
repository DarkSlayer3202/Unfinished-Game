#!/usr/bin/env python3
import pygame
import random
from pygame.locals import *

spaceship = 'assets/spaceship.png'
spaceship_inactive = 'assets/spaceship_inactive.png'
mouse_c = 'assets/cursor.png'
backg = 'assets/background.jpg'
pygame.init()
lazer = pygame.mixer.Sound("assets/pew.WAV")
display_width = 1280
display_height = 720
Ammo = 20
Fuel = 1000
Speed = 0
ship_pos = display_width // 2, display_height // 2
Speed_MAX = 0
rotation = 0
Boost = 1
pic = pygame.image.load('assets/meteor.png')

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Open Space")
clock = pygame.time.Clock()

position = pygame.math.Vector2(screen.get_rect().center)
direction = pygame.math.Vector2(0, 5)

bk = pygame.image.load(backg).convert_alpha()
space_ship = pygame.image.load(spaceship_inactive).convert_alpha()
mousec = pygame.image.load(mouse_c).convert_alpha()
pic = pygame.image.load('assets/meteor.png').convert_alpha()

pygame.mouse.set_visible(True)
dead = False
ready = True
pause = False
# rotimage2 = pygame.transform.rotozoom(pic, random.randint(0, 359), random.randint(1, 2))

next_meteor_time = 0
meteor_interval = 3000  # 2000 milliseconds == 2 sceonds


class Meteor(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)

        self.rotation = random.randint(0, 359)
        self.size = random.randint(1, 2)
        self.image = pic
        self.image = pygame.transform.rotozoom(self.image, self.rotation, self.size)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


all_meteors = pygame.sprite.Group()


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = 255,255,255
        self.facing = facing
        self.vel = 4 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


bullets = []  # This goes right above the while loop
while ready:
    clock.tick(60)  # FPS, Everything happens per frame
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and Ammo >> 1:
                print("Pew")
                pygame.mixer.Sound.play(lazer)
                knockback = 4
                while knockback > 0:
                    position -= direction
                    knockback = knockback - 1
                Ammo = Ammo - 1
                if len(bullets) < 20:  # This will make sure we cannot exceed 5 bullets on the screen at once
                    bullets.append(projectile(round(200 + 32 // 2), round(200 + 24 // 2), 6, (0, 0, 0), angle))
    # Goes inside the while loop

    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel  # Moves the bullet by its vel
        else:
            bullets.pop(bullets.index(bullet))  # This will remove the bullet if it is off the screen

    direction.rotate_ip(rotation)
    current_time = pygame.time.get_ticks()

    if current_time >= next_meteor_time:
        next_meteor_time += meteor_interval
        new_x = random.randrange(0, display_width)
        new_y = random.randrange(0, display_height)
        all_meteors.add(Meteor(new_x, new_y))

    if pygame.key.get_pressed()[pygame.K_a]:
        rotation = rotation - 0.05
    if pygame.key.get_pressed()[pygame.K_d]:
        rotation = rotation + 0.05

    if rotation > 10:
        rotation = rotation - 0.05
    if rotation < -10:
        rotation = rotation + 0.05

    if pygame.key.get_pressed()[pygame.K_w] and Fuel > 0:
        space_ship = pygame.image.load(spaceship).convert_alpha()
        position += direction
        Fuel = Fuel - 1
        print(Fuel)

    if not pygame.key.get_pressed()[pygame.K_w]:
        # Speed = Speed / 1.005
        space_ship = pygame.image.load(spaceship_inactive).convert_alpha()
    if Fuel == 0:
        # Speed = Speed / 1.005
        space_ship = pygame.image.load(spaceship_inactive).convert_alpha()

    # if Speed >= Speed_MAX:
    # Speed = Speed_MAX - 1

    angle = direction.angle_to((1, 0))
    rotimage = pygame.transform.rotate(space_ship, angle)

    screen.blit(bk, (0, 0))
    screen.blit(rotimage, rotimage.get_rect(center=(round(position.x), round(position.y))))
    # screen.blit(rotimage2, (random.randint(0, 1280), random.randint(0, 720)))
    all_meteors.update()

    all_meteors.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.update()
