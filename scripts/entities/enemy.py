import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/entities/enemies/00.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.pos_x = float(x)
        self.speed = 0.5
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.pos_x += self.speed * self.move_direction
        self.rect.x = round(self.pos_x)

        self.move_counter += abs(self.speed * self.move_direction)
        if self.move_counter > 32:
            self.move_direction *= -1
            self.move_counter = 0