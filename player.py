import pygame 
import math
import entities
import constants

PLAYER_SIZE = 5

class Player(entities.Entity):
    def __init__(self):
        entities.Entity.__init__(self)
        self.xpos = 300
        self.ypos = 300

    def draw_Player(self, screen):
        xpos = self.xpos
        ypos = self.ypos
        white = (255, 255, 255, 255)
        pygame.draw.circle(screen, (constants.red), (self.xpos, self.ypos), 3)
        pygame.draw.rect(screen, (white), (self.xpos - PLAYER_SIZE, self.ypos - PLAYER_SIZE, 2 * PLAYER_SIZE, 2 * PLAYER_SIZE))