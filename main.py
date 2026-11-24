import pygame
import sys
from scripts.stars import Stars
from scripts.world import World
from scripts.buttons.button import Button
from scripts.levels import Level_01, Level_02, Level_03
from scripts.entities.player import Player
from scripts.items.coin import Coin

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TILE_SIZE = 16
WHITE = (255, 255, 255)
TEAL = (0, 255, 255)

class Game():
    def __init__(self):            
        pygame.init()

        pygame.display.set_caption('platformer game')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240)) # for rendering

        self.font = pygame.font.SysFont('Terminal', 48)
        self.font_score = pygame.font.SysFont('Terminal', 24)
        self.font_hint = pygame.font.SysFont('Terminal', 14)

        self.clock = pygame.time.Clock()

        self.score = 0
        self.game_over = 0

        self.stars = Stars((500,-100), pygame.image.load('assets/background/stars.png'), speed=0.2)

        self.player = Player(20, 150)

        img = pygame.image.load('assets/buttons/restart.png')

        self.restart_button = Button(
            (self.display.get_width() - img.get_width()) // 2,
            (self.display.get_height() - img.get_height()) // 2,
            img)

        self.alien_group = pygame.sprite.Group()
        self.platform_group = pygame.sprite.Group()
        self.disappear_platform_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.prop_group = pygame.sprite.Group()
        self.door_group = pygame.sprite.Group()

        self.level_list = []
        self.level_list.append(Level_01())
        self.level_list.append(Level_02())
        self.level_list.append(Level_03())

        self.load_level(0)

    def load_level(self, level_no):
        self.curr_level_no = level_no
        self.curr_level = self.level_list[level_no]

        self.alien_group.empty()
        self.platform_group.empty()
        self.disappear_platform_group.empty()
        self.coin_group.empty()
        self.prop_group.empty()
        self.door_group.empty()

        self.world = World(self.curr_level.world_data, self)

        self.player.reset(20, 180)
        self.game_over = 0   

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.display.blit(img, (x, y))

    def draw_text_centered(self, text, font, text_col, y):
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(self.display.get_width() // 2, y))
        self.display.blit(img, rect)

    def run(self):
        while True:
            self.display.blit(self.curr_level.background, (0, 0))

            self.stars.update()
            self.stars.render(self.display)

            self.world.draw()

            # game is running
            if self.game_over == 0:
                self.alien_group.update()
                self.platform_group.update(self.player)
                self.disappear_platform_group.update()
                if pygame.sprite.spritecollide(self.player, self.coin_group, True):
                    self.score += 1
                self.draw_text('X ' + str(self.score) + ' / 13', self.font_score, WHITE, TILE_SIZE, TILE_SIZE)
                if self.curr_level_no == 0:
                    self.draw_text('Press 1 for LVL1, 2 for LVL2, 3 for LVL3, 4 to end', self.font_hint, WHITE, SCREEN_WIDTH // 9, SCREEN_HEIGHT // 2 - 28)
                if self.curr_level_no == 1:
                    self.draw_text('Grab side of moving platform to pull yourself up!', self.font_hint, WHITE, SCREEN_WIDTH // 9, SCREEN_HEIGHT // 2 - 28)


            # draw groups
            self.alien_group.draw(self.display)
            self.platform_group.draw(self.display)
            self.disappear_platform_group.draw(self.display)
            self.door_group.draw(self.display)
            self.prop_group.draw(self.display)
            self.coin_group.draw(self.display)

            # game is lost
            if self.game_over == -1:
                if self.restart_button.draw(self.display):
                    self.load_level(self.curr_level_no)
                    self.score = 0

            # game is won
            if self.game_over == 1:
                if self.score == 13:
                    self.draw_text_centered('YOU WON IT!', self.font, TEAL, 100)
                else:
                    self.draw_text_centered("So close...", self.font, TEAL, 100)                
                self.draw_text_centered('Coins: ' + str(self.score), self.font, TEAL, 130)

            self.player.update(self.display, self.world.tile_list, self)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                key = pygame.key.get_pressed()
                if key[pygame.K_1]:
                    self.load_level(0)
                if key[pygame.K_2]:
                    self.load_level(1)
                if key[pygame.K_3]:
                    self.load_level(2)
                if key[pygame.K_4]:
                    self.game_over = 1

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()