import pygame
import random

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
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

class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        super(Bonus, self).__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255, 215, 0))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_top_speed):
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

class GameState:
    def __init__(self):
        self.enemy_top_speed = 10
        self.enemy_frequency = 250
        self.enemy_total = 1
        self.enemy_speed_counter = 0

        self.player = Player()
        self.player_score = 0
        self.player_lost = False

def initialize_game_state(game_state):
    game_state.enemy_top_speed = 10
    game_state.enemy_frequency = 250
    game_state.enemy_total = 1
    game_state.enemy_speed_counter = 0
    game_state.player = Player()
    game_state.player_score = 0
    game_state.player_lost = False

def draw_score(screen, player_score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {player_score}", True, (255, 255, 255))
    text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
    screen.blit(score_text, text_rect)

def game_over(screen):
    font = pygame.font.Font(None, 36)
    end_text = font.render("Press SPACE to replay", True, (255, 255, 255))
    text_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, 75))
    screen.blit(end_text, text_rect)

# def replay():
#     global player_lost, player_score
#     player_lost = False
#     player_score = 0

# constants for screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



def main():
    pygame.init()


    # create screen object; this is the portion of the screen I control, while OS controls window borders and title bar
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # enemy_top_speed = 10
    # enemy_frequency = 250
    # enemy_total = 1
    # enemy_speed_counter = 0

    # player = Player()
    # player_score = 0
    # player_lost = False

    game_state = GameState()
    initialize_game_state(game_state)

    # custom event for adding an enemy
    ADDENEMY = pygame.USEREVENT + 1
    # pygame defines events as integers; new event needs to be a unique integer
    # USEREVENT designates the last event, so USEREVENT + 1 should be a new unique integer
    pygame.time.set_timer(ADDENEMY, game_state.enemy_frequency)
    # fires the ADDENEMY event every 250 milliseconds


    # creating sprite groups -> enemies used for collision detection & position updates; all_sprites used for rendering
    enemies = pygame.sprite.Group()
    bonuses = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(game_state.player)

    new_bonus = Bonus()
    bonuses.add(new_bonus)
    all_sprites.add(new_bonus)

    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if game_state.player_lost and event.key == K_SPACE:
                    game_state = GameState()
                    initialize_game_state(game_state)
                    all_sprites.add(game_state.player)
                elif event.key == K_ESCAPE:
                    running = False

            elif event.type == QUIT:
                running = False

            # Add new enemy?
            elif event.type == ADDENEMY:
                for i in range(game_state.enemy_total):
                    new_enemy = Enemy(game_state.enemy_top_speed)
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)

            # elif event.type == ADDBONUS:
            #     new_bonus = Bonus()
            #     bonus.add(new_bonus)
            #     all_sprites.add(new_bonus)

        # .get_pressed() method returns a dictionary containing all current KEYDOWN events in the queue
        # --here, a dict of keys pressed at the beginning of each frame
        pressed_keys = pygame.key.get_pressed()

        game_state.player.update(pressed_keys)

        enemies.update()
        game_state.enemy_speed_counter = game_state.enemy_speed_counter + 1
        if game_state.enemy_speed_counter == 500:
            game_state.enemy_speed_counter = 0
            game_state.enemy_top_speed = game_state.enemy_top_speed + 1
            game_state.enemy_frequency = game_state.enemy_frequency - 50
            if game_state.enemy_frequency < 10:
                game_state.enemy_frequency = 250
                game_state.enemy_total = game_state.enemy_total + 1

        screen.fill((0, 0, 0))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if pygame.sprite.spritecollideany(game_state.player, enemies):
            game_state.player.kill()
            game_state.player_lost = True
            
        #    running = False

        bonus_hit = pygame.sprite.spritecollide(game_state.player, bonuses, True)
        if bonus_hit:
            game_state.player_score = game_state.player_score + 10
            new_bonus = Bonus()
            bonuses.add(new_bonus)
            all_sprites.add(new_bonus)

        draw_score(screen, game_state.player_score)
        if game_state.player_lost == True:
            game_over(screen)

        pygame.display.flip()

        clock.tick(60)

main()