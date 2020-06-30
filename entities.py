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
        # Rule 3 -> If True Orbit
        # Rule 4 -> If True, Display the bullet


        self.rules = [True, False, False, False, True]
        self.life  = -1
        self.birth  = 0
        self.homingWeight = 0.01
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


        # Delay Array Update -> If False, do not Update the current Delay

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
            self.xpos = xpos
            self.ypos = ypos
            self.addVertex((self.xpos, self.ypos))
        else:
            self.isOrbit = False

    def setParams(self, xvel, yvel, xacc, yacc):
        self.xvel = xvel
        self.yvel = yvel
        self.xacc = xacc / 100
        self.yacc = yacc / 100

    def setOrbitParams(self, vel, acc, rad, centerx, centery, angle0):
        self.orbitVel = math.radians(vel)
        self.orbitAcc = math.radians(acc) / 100
        self.orbitRad = rad
        self.orbitCenterx = centerx
        self.orbitCentery = centery
        self.orbitAngle = angle0

    def setOrbitRadParams(self, vel, acc):
        self.orbitRadVel = vel
        self.orbitRadAcc = acc / 100

    def motion(self):
        
        # Check if Sticky, if yes then immediately stop 

        if self.isSticky: 
            return

        if self.isOrbit:
            self.xpos = (self.orbitCenterx + self.orbitRad * math.cos(self.orbitAngle))
            self.ypos = (self.orbitCentery + self.orbitRad * math.sin(self.orbitAngle))
            self.orbitAngle += self.orbitVel
            self.orbitVel += self.orbitAcc
            self.orbitRad += self.orbitRadVel
            self.orbitRadVel += self.orbitRadAcc

        elif not self.polyMove:
            mousex, mousey = pygame.mouse.get_pos()
            target = 0
            ctarget = 0
            if self.isHoming:
                target = getTarget(mousex, mousey, self.xpos, self.ypos) + math.radians(self.homingError)
            if self.rules[3] == True:
                ctarget = self.orbitAngle

            rfactor = self.homingWeight * int(self.isHoming) + 1
            self.xpos = (self.xpos + self.xvel) 
            self.ypos = (self.ypos + self.yvel) 
            self.xvel = (self.xvel + self.xacc )    
            self.yvel = (self.yvel + self.yacc) 
            self.xacc = (self.xacc + self.homingWeight * int(self.isHoming) * math.cos(target))/ rfactor
            self.yacc = (self.yacc + self.homingWeight * int(self.isHoming) * math.sin(target))/rfactor

        elif self.polyMove:
            r = self.xpos
            s = self.ypos
            (p, q) = self.polyMoveArray[self.currvertex]
            if math.sqrt((r - p) * (r-p) + (s - q) * (s- q)) <= math.sqrt(self.xvel * self.xvel + self.yvel + self.yvel):
                a = self.currvertex + 2
                self.currvertex = self.currvertex + 1
                if self.currvertex >= len(self.polyMoveArray) and not self.polyMoveLoop:
                    self.currvertex = len(self.polyMoveArray) - 1
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
                self.target = getTarget(p, q, self.xpos, self.ypos)
                self.stop = True 

            self.xpos = self.xpos + self.xvel * math.cos(self.target) 
            self.ypos = self.ypos + self.yvel * math.sin(self.target)
            self.xvel = abs  (self.xvel + self.xacc) 
            self.xacc = self.xacc * math.cos(self.target)

            self.yvel = abs (self.yvel + self.yacc) 
            self.yacc = self.yacc * math.sin(self.target) 


