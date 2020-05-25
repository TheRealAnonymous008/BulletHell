import math
import constants
import pygame

def getTarget(dirx, diry, xpos, ypos):
    return math.atan2((diry - ypos), (dirx - xpos))

class Entity(pygame.sprite.Sprite):
    def __init__ (self):
        self.xpos = 0
        self.ypos = 0
        self.xvel = 0
        self.yvel = 0
        self.xacc = 0
        self.yacc = 0

        # Rule 0 -> If Out Of Bounds, Delete
        # Rule 1 -> If True, Follow the Player 
        # Rule 2 -> iF True Stop after Sticky_Time


        self.rules = [True, False, False]
        self.life  = -1
        self.birth  = 0
        self.homingWeight = 0.01
        self.homingError = 0
        self.homingDelay = -1
        self.isHoming = False
        self.isSticky = False
        self.stickyTimer = -1
        self.stickyTimerStop = -1
        pygame.sprite.Sprite.__init__(self)

    def setStickyTimerStop(self, val):
        self.stickyTimerStop = val

    def setIsSticky(self, val):
        self.rules[2] = val

    def setStickyTimer(self, val):
        self.stickyTimer = val

    def setHomingWeight(self, weight):
        self.homingWeight = weight

    def setHomingError(self, error):
        self.homingError = error
    
    def setHomingDelay(self, delay):
        self.homingDelay = delay

    def setBirth(self, time):
        self.birth = time

    def setdeleteIfOut(self, val):
        self.rules[0]= val

    def isdeleteIfOut(self):
        return self.rules[0]

    def setLocation(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos

    def setParams(self, xvel, yvel, xacc, yacc):
        self.xvel = xvel
        self.yvel = yvel
        self.xacc = xacc / 100
        self.yacc = yacc / 100

    def motion(self):
        
        # Check if Sticky, if yes then immediately stop 

        if self.isSticky: 
            return

        mousex, mousey = pygame.mouse.get_pos()
        target = 0
        if self.isHoming:
            target = getTarget(mousex, mousey, self.xpos, self.ypos) + math.radians(self.homingError)

        rfactor = self.homingWeight * int(self.isHoming) + 1 
        self.xpos = self.xpos + self.xvel
        self.xvel = (self.xvel + self.xacc )        
        self.ypos = self.ypos + self.yvel 
        self.yvel = (self.yvel + self.yacc) 

        # * (self.homingWeight * int(self.rules[1]) * math.cos(target))/rfactor


        self.xacc = (self.xacc + self.homingWeight * int(self.isHoming) * math.cos(target))/ rfactor
        self.yacc = (self.yacc + self.homingWeight * int(self.isHoming) * math.sin(target))/rfactor