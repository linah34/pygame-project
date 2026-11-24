import pygame

class Chain(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/items/chains/chain.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Connector(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/items/chains/connector.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class LeftChain(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/items/chains/left_chain.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class RightChain(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/items/chains/right_chain.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y