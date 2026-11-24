import pygame

TILE_SIZE = 16

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/tiles/platform4/platform.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class MovingPlatform(Platform):
    def __init__(self, x, y, change_x, change_y):
        super().__init__(x, y)
        self.move_direction = 1
        self.move_counter = 0
        self.change_x = change_x
        self.change_y = change_y

    def update(self, player):
        self.rect.x += self.move_direction * self.change_x
        self.rect.y += self.move_direction * self.change_y

        self.move_counter += 1
        if self.move_counter > 64:
            self.move_direction *= -1
            self.move_counter = 0

class DisappearingPlatform(Platform):
    # https://stackoverflow.com/questions/45520104/counting-time-in-pygame
    # https://www.pygame.org/docs/ref/time.html 
    # technique for counting time
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.visible_image = self.image
        self.hidden_image = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        self.active = True
        self.on_time = 3000
        self.off_time = 2000
        self.state_time = pygame.time.get_ticks()

    def update(self):
        elapsed = pygame.time.get_ticks() - self.state_time
        if self.active and elapsed >= self.on_time:
            self.active = False
            self.image = self.hidden_image
            self.state_time = pygame.time.get_ticks()
        elif self.active == False and elapsed >= self.off_time:
            self.active = True
            self.image = self.visible_image
            self.state_time = pygame.time.get_ticks()

    def draw(self, surf):
        if self.active:
            surf.blit(self.image, self.rect)
