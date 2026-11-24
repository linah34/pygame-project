import pygame
import math

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TILE_SIZE = 16

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.reset(x, y)
        

    def reset(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # technique for animation inspired by platform_scroller.py + other files
        self.images_right = []
        self.images_left = []
        self.direction = 0

        self.index = 0
        self.counter = 0
        for num in range(0,4):
            img_right = pygame.image.load(f'assets/entities/player/walk/0{num}.png').convert()

            img_right = pygame.transform.scale(img_right, (TILE_SIZE, TILE_SIZE))
            img_left = pygame.transform.flip(img_right, True, False)

            img_right.set_colorkey((0, 0, 0))
            img_left.set_colorkey((0, 0, 0))

            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.dead_image = pygame.image.load('assets/entities/player/dead/dead.png').convert()
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.in_air = True

    def update(self, surf, tile_list, game_data):
        dx = 0
        dy = 0
        walk_cooldown = 2

        if game_data.game_over == 0:

            # get key
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.jumped == False and self.in_air == False:
                self.vel_y = -9
                self.jumped = True
            if key[pygame.K_UP] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 2
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 2
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # add gravity
            self.vel_y += .8
            if self.vel_y > 8:
                self.vel_y = 8
            dy += math.ceil(self.vel_y) # to make whole pixel

            # handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # check for collisions
            self.in_air = True

            for tile in tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                    if self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # check for enemy collision
            if pygame.sprite.spritecollide(self, game_data.alien_group, False, pygame.sprite.collide_rect_ratio(0.7)):
                game_data.game_over = -1

            # check for door collision
            if pygame.sprite.spritecollide(self, game_data.door_group, False):
                if game_data.curr_level_no < len(game_data.level_list) - 1:
                    game_data.load_level(game_data.curr_level_no + 1)
                    return
                else:
                    game_data.game_over = 1
                        
            # check for platform collision
            for platform in game_data.platform_group:
                p_dx = platform.change_x * platform.move_direction
                p_dy = platform.change_y * platform.move_direction

                # horizontal collision
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                # vertical collision
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    pred_dy = dy - p_dy                      
                    if pred_dy < 0:                             
                        dy = platform.rect.bottom - self.rect.top
                        self.vel_y = 0
                    else:                                     
                        dy = platform.rect.top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
                        dx += p_dx      

            # check for disappearing platform collision
            for disappear_platform in game_data.disappear_platform_group:
                if disappear_platform.active and disappear_platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if disappear_platform.active and disappear_platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = disappear_platform.rect.bottom - self.rect.top
                    if self.vel_y >= 0:
                        dy = disappear_platform.rect.top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False   

            # update player coords
            self.rect.x += dx
            self.rect.y += dy

        elif game_data.game_over == -1:
            self.image = self.dead_image

        surf.blit(self.image, self.rect)
        # pygame.draw.rect(surf, (255, 255, 255), self.rect, 1)