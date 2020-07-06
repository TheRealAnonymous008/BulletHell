import math
import constants
import pygame

from timeiterator import *

def getTarget(dirx, diry, xpos, ypos):
    return math.atan2((diry - ypos), (dirx - xpos))

class Entity(pygame.sprite.Sprite):
    def __init__ (self):
        
        # Initial values:

        self.xposi = 0
        self.yposi = 0
        self.xveli = 0
        self.yveli = 0

        # Necessary Values

        self.xpos = 0
        self.ypos = 0
        self.xvel = 0
        self.yvel = 0
        self.xacc = 0
        self.yacc = 0

        # Rule 0 -> If Out Of Bounds, Delete
        # Rule 1 -> If True, Follow the Player 
        # Rule 2 -> iF True Stop after Sticky_Time
        # Rule 3 -> If True Orbit
        # Rule 4 -> If True, Display the bullet


        self.rules = [True, False, False, False, True]
        self.life  = -1
        self.birth  = 0
        self.homingWeight = 1000
        self.homingError = 0
        self.homingDelay = -1
        self.isHoming = False
        self.isSticky = False
        self.isOrbit = False
        self.orbitTimer = -1
        self.orbitTimerStop = -1
        self.stickyTimer = -1
        self.stickyTimerStop = -1


        # Orbit Parmas:
        self.orbitVel = 0
        self.orbitAcc = 0
        self.orbitRad = 0
        self.orbitCenterx = 0
        self.orbitCentery = 0
        self.orbitAngle = 0
        self.orbitRadVel = 0
        self.orbitRadAcc =0

        # Initial Orbit Params
        self.orbitVeli = 0
        self.orbitAnglei = 0
        self.orbitRadi = 0
        self.orbitRadveli = 0

        self.visibleTimerStop = -1
        self.isVisible = True
        pygame.sprite.Sprite.__init__(self)

        self.polyMove = False
        self.polyMoveArray = []
        self.polyMoveLoop = False
        self.target = 0
        self.currvertex = 0

        self.motion_delay = -1
        self.polyMoveDelayArray =[-1, -1 ]
        self.stop = False
        self.lastStopTime = 0

        # Keep Track of the time when sticky was activated
        self.lastStickyTime = 0

        self.homeTime = -1
        self.isNotMoving = False
        self.stopHoming = False

        self.currentTime = 0

    def setHomeTime(self, time):
        self.hometime = time

    def setMotionDelay(self, time):
        self.motion_delay = time
        self.polyMoveDelayArray[1] = time
    def setPolyMoveLooping(self, val):
        self.polyMoveLoop = val

    def setPolyMove(self, val):
        self.polyMove = val

    def addVertex(self, vert, delay = -1):
        # vertex is of the form (x, y):
        # delay specifies how much time bullet lingers
        self.polyMoveArray.append(vert)
        self.polyMoveDelayArray.append(delay)

    def setVisibleStopTimer(self, time):
        self.visibleTimerStop = time

    def setVisible(self, val):
        self.rules[4] = val
        self.isVisible = val

    def setOrbitTimer(self, val):
        self.orbitTimer = val
    
    def setOrbitTimerStop(self, val):
        self.orbitTimerStop = val

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
        if self.__class__.__name__ == "Shooter":
            if self.mode == 0:
                self.birth = 0
        self.birth = time

    def setdeleteIfOut(self, val):
        self.rules[0]= val

    def isdeleteIfOut(self):
        return self.rules[0]

    def setLocation(self, xpos, ypos):
        if not self.isOrbit or self.orbitTimer != -1:
            self.xposi = xpos
            self.xpos = xpos
            self.ypos = ypos
            self.yposi = ypos
            self.addVertex((self.xposi, self.yposi))
        else:
            self.isOrbit = False

    def setParams(self, xvel, yvel, xacc, yacc):
        self.xveli = xvel
        self.yveli = yvel
        self.xacc = xacc
        self.yacc = yacc

    def setOrbitParams(self, vel, acc, rad, centerx, centery, angle0):
        self.orbitVel = vel * 4
        self.orbitAcc = acc
        self.orbitRad = rad
        self.orbitCenterx = centerx
        self.orbitCentery = centery
        self.orbitAngle = angle0

        self.orbitAnglei = self.orbitAngle
        self.orbitVeli = self.orbitVel
        self.orbitRadi = rad

    def setOrbitRadParams(self, vel, acc):
        self.orbitRadVel = vel 
        self.orbitRadAcc = acc
        self.orbitRadveli = vel

    def motion(self, time):
        # Check if Sticky, if yes then immediately stop 
        
        if self.isSticky:
            return
        
        if self.isNotMoving:
            return

        self.currentTime += constants.FPS / 1000
        time = self.currentTime

        
        if self.currentTime >= self.life / constants.FPS and self.life != -1:
            self.life = 0


        if self.isOrbit:
            self.xpos = (self.orbitCenterx + self.orbitRad * math.cos(math.radians(self.orbitAngle)))
            self.ypos = (self.orbitCentery + self.orbitRad * math.sin(math.radians(self.orbitAngle)))


            self.orbitAngle = self.orbitAnglei + self.orbitVel * time * math.pi * 2
            self.orbitVel = self.orbitVeli + self.orbitAcc * time * math.pi * 2
            self.orbitRad = self.orbitRadi + self.orbitRadVel * time 
            self.orbitRadVel = self.orbitRadveli * self.orbitRadAcc * time 

        elif not self.polyMove and not self.isOrbit:
            mousex, mousey = pygame.mouse.get_pos()
            target = 0
            ctarget = 0
            if self.isHoming:
                target = getTarget(mousex, mousey, self.xpos, self.ypos) + math.radians(self.homingError)
            if self.rules[3] == True:
                ctarget = self.orbitAngle

            rfactor = self.homingWeight * int(self.isHoming) + 1
            rfactor = 1
            self.xpos = (self.xposi + self.xvel * time) 
            self.ypos = (self.yposi + self.yvel * time) 
            self.xvel = (self.xveli + self.xacc * time)    
            self.yvel = (self.yveli + self.yacc * time) 
            self.xacc = (self.xacc + self.homingWeight * int(self.isHoming) * math.cos(target))/ rfactor
            self.yacc = (self.yacc + self.homingWeight * int(self.isHoming) * math.sin(target))/rfactor

        elif self.polyMove:
            r = self.xpos
            s = self.ypos
            (p, q) = self.polyMoveArray[self.currvertex]
            if math.sqrt((r - p) * (r-p) + (s - q) * (s- q)) <= math.sqrt(self.xveli * self.xveli + self.yveli * self.yveli):
                a = self.currvertex + 2
                self.currvertex = self.currvertex + 1
                if self.currvertex >= len(self.polyMoveArray) - 1 and not self.polyMoveLoop:
                    self.currvertex = len(self.polyMoveArray) - 2
                elif self.currvertex >= len(self.polyMoveArray):
                    self.currvertex = 1

                if a >= len(self.polyMoveDelayArray) and not self.polyMoveLoop:
                    a = len(self.polyMoveDelayArray) - 1
                    self.motion_delay = self.polyMoveDelayArray[a]
                elif a >= len(self.polyMoveDelayArray):
                    self.motion_delay = self.polyMoveDelayArray[2]
                    a = 2
                else:
                    self.motion_delay = self.polyMoveDelayArray[a]
                    
                (p, q) = self.polyMoveArray[self.currvertex]
                self.stop = True 

            self.target = getTarget(p, q, self.xpos, self.ypos)
            
            val = constants.FPS / 1000
            self.xposi = self.xposi + self.xveli * math.cos(self.target) * val
            self.yposi = self.yposi + self.yveli * math.sin(self.target) *val
            self.xveli = abs  (self.xveli + self.xacc * val) 
            self.xacc = self.xacc * math.cos(self.target)

            self.yveli = abs (self.yveli + self.yacc  * val) 
            self.yacc = self.yacc * math.sin(self.target) 

            self.xpos = self.xposi
            self.ypos = self.yposi




