import pygame
from scripts.entities.enemy import Enemy
from scripts.items.coin import Coin
from scripts.items.props import Chain, Connector, LeftChain, RightChain
from scripts.items.door import Door
from scripts.platforms import MovingPlatform, DisappearingPlatform

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TILE_SIZE = 16

class Tile():
    def __init__(self, img_name, col, row, half=False):
        self.image = pygame.transform.scale(img_name, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(col * TILE_SIZE, row * TILE_SIZE))
        if half:
            self.rect.height = TILE_SIZE // 2


class World():
    # https://youtu.be/Ongc4EVqRjo 
    # technique for making a tile map
    # levels class an extension of world data

    def __init__(self, data, game_data):
        self.game_data = game_data
        self.tile_list = []

        # load assets
        outerwall_img = pygame.image.load('assets/tiles/walls/outer_wall.png')

        platform1a_img = pygame.image.load('assets/tiles/platform1/left_end.png')
        platform1b_img = pygame.image.load('assets/tiles/platform1/middle.png')
        platform1c_img = pygame.image.load('assets/tiles/platform1/right_end.png')

        platform2a_img = pygame.image.load('assets/tiles/platform2/left_end.png')
        platform2b_img = pygame.image.load('assets/tiles/platform2/middle.png')
        platform2c_img = pygame.image.load('assets/tiles/platform2/right_end.png')
        platform2a_img.set_colorkey((0, 0, 0))
        platform2b_img.set_colorkey((0, 0, 0))
        platform2c_img.set_colorkey((0, 0, 0))

        platform3a_img = pygame.image.load('assets/tiles/platform3/left_end.png')
        platform3b_img = pygame.image.load('assets/tiles/platform3/middle.png')
        platform3c_img = pygame.image.load('assets/tiles/platform3/right_end.png')

        platform4_img = pygame.image.load('assets/tiles/platform4/platform.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                # outer wall
                if tile == 1:
                    img = Tile(outerwall_img, col_count, row_count)
                    self.tile_list.append((img.image, img.rect))
                # platform 1 (full block)
                if tile == 2:
                    img = Tile(platform1a_img, col_count, row_count)
                    self.tile_list.append((img.image, img.rect))
                if tile == 3:
                    img = Tile(platform1b_img, col_count, row_count)
                    self.tile_list.append((img.image, img.rect))
                if tile == 4:
                    img = Tile(platform1c_img, col_count, row_count)
                    self.tile_list.append((img.image, img.rect))
                # platform 2 (chain)
                if tile == 5:
                    img = Tile(platform2a_img, col_count, row_count, half=True)
                    self.tile_list.append((img.image, img.rect))
                if tile == 6:
                    img = Tile(platform2b_img, col_count, row_count, half=True)
                    self.tile_list.append((img.image, img.rect))
                if tile == 7:
                    img = Tile(platform2c_img, col_count, row_count, half=True)
                    self.tile_list.append((img.image, img.rect))
                if tile == 8:
                    chain = Chain(col_count * TILE_SIZE, row_count * TILE_SIZE)
                    self.game_data.prop_group.add(chain)
                if tile == 9:
                    connector = Connector(col_count * TILE_SIZE, row_count * TILE_SIZE)
                    self.game_data.prop_group.add(connector)
                if tile == 10:
                    left_chain = LeftChain(col_count * TILE_SIZE, row_count * TILE_SIZE)
                    self.game_data.prop_group.add(left_chain)
                if tile == 11:
                    right_chain = RightChain(col_count * TILE_SIZE, row_count * TILE_SIZE)
                    self.game_data.prop_group.add(right_chain)
                if tile == 12:
                    img = Tile(platform3a_img, col_count, row_count, half=True)
                    self.tile_list.append((img.image, img.rect))
                if tile == 13:
                    img = Tile(platform3b_img, col_count, row_count, half=True)
                    self.tile_list.append((img.image, img.rect))
                if tile == 14:
                    img = Tile(platform3c_img, col_count, row_count, half=True)
                    self.tile_list.append((img.image, img.rect))
                if tile == 15:
                    img = Tile(platform4_img, col_count, row_count, half=True)
                    self.tile_list.append((img.image, img.rect))
                if tile == 16:
                    door = Door(col_count * TILE_SIZE, row_count * TILE_SIZE)
                    self.game_data.door_group.add(door)
                if tile == 17:
                    coin = Coin(col_count * TILE_SIZE, row_count * TILE_SIZE)
                    self.game_data.coin_group.add(coin)
                if tile == 18:
                    alien = Enemy(col_count * TILE_SIZE, row_count * TILE_SIZE)
                    self.game_data.alien_group.add(alien)
                if tile == 19:
                    platform = MovingPlatform(col_count * TILE_SIZE, row_count * TILE_SIZE, 1, 0)
                    self.game_data.platform_group.add(platform)
                if tile == 20:
                    platform = MovingPlatform(col_count * TILE_SIZE, row_count * TILE_SIZE, 0, 1)
                    self.game_data.platform_group.add(platform)
                if tile == 21:
                    platform = DisappearingPlatform(col_count * TILE_SIZE, row_count * TILE_SIZE)
                    self.game_data.disappear_platform_group.add(platform)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            self.game_data.display.blit(tile[0], tile[1])            