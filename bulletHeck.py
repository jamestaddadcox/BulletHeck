import pygame
import random

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        # keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(enemy_top_speed - 5, enemy_top_speed)

    def update(self):
            self.rect.move_ip(-self.speed, 0)
            if self.rect.right < 0:
                self.kill()
                # .kill() removes a sprite from every group it belongs to


# constants for screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

enemy_top_speed = 10
enemy_frequency = 250
enemy_total = 1
enemy_speed_counter = 0

pygame.init()


# create screen object; this is the portion of the screen I control, while OS controls window borders and title bar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# custom event for adding an enemy
ADDENEMY = pygame.USEREVENT + 1
# pygame defines events as integers; new event needs to be a unique integer
# USEREVENT designates the last event, so USEREVENT + 1 should be a new unique integer
pygame.time.set_timer(ADDENEMY, enemy_frequency)
# fires the ADDENEMY event every 250 milliseconds


player = Player()

# creating sprite groups -> enemies used for collision detection & position updates; all_sprites used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        # Add new enemy?
        elif event.type == ADDENEMY:
            for i in range(enemy_total):
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

    # .get_pressed() method returns a dictionary containing all current KEYDOWN events in the queue
    # --here, a dict of keys pressed at the beginning of each frame
    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)

    enemies.update()
    enemy_speed_counter = enemy_speed_counter + 1
    if enemy_speed_counter == 250:
        enemy_speed_counter = 0
        enemy_top_speed = enemy_top_speed + 1
        enemy_frequency = enemy_frequency - 50
        if enemy_frequency < 10:
            enemy_frequency = 250
            enemy_total = enemy_total + 1

    screen.fill((0, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
    #    running = False

    pygame.display.flip()

    clock.tick(60)