import random
import sys
import pygame
import math
import time
import copy
from bullet import *
from entities import * 
from timeiterator import *
import constants


white = constants.white
black = (0, 0, 0)
pi = math.pi
defualt_bullet_size = constants.default_bullet_size
swidth =  constants.SWIDTH
sheight = constants.SHEIGHT
TIME_DECEL = constants.TIME_DECEL

def getTarget(dirx, diry, xpos, ypos):
    return math.atan2((diry - ypos), (dirx - xpos))

# Shooter class spawns bullets and projectiles
# For Creating Bullets which disappear instantly, set Bullet Life to 0.05 and ROF to 50

class Shooter(Bullet): 

    # xpos  and ypos are the corresponding x and y posititons. 
    # xvel and yvel are the corresponding x and y
    # xacc and yacc are the corresponding x and y accelerations
    # color sets the color of the bullets. 
    # rof adjusts the rate of fire of the shooter. Measured in bullets per millisecond
    # bulletctr determoines how many bullets are fired in a single instance
    # firing determines if the shooter will fire
    # bullets contains all the Bullet Objects created by the shooter
    # bulletLife is the amount of ticks before bullet is erased from the screen
    # ammo is the number of bullets

    def __init__(self):
        Bullet.__init__(self)
        self.bulletColor = constants.white
        self.rof = 100
        self.rofIter = TimeIterator()
        self.bulletctr = 20
        self.firing = False
        self.bullets = pygame.sprite.Group()
        self.bulletlife = -1
        self.ammo = -1
        self.nextTime = 0 
        self.bullet_size = defualt_bullet_size
        self.bullets_sticky_timer_stop = -1

        # In radius determines the radius of a circle from which all bullets will start.
        # Out radius determines the point up to which all bullets will be deleted, - 1 indicates no outRadis
        self.inRadius = 1

        # Targetting weight determines how much targetting is prioritized
        # Targetting error determines how inaccurate the aim is

        self.targettingWeight = 1000
        self.targettingError = 0

        # Birth determines the time shooter is created
        self.birth = 0

        # The Following control Burst Shot Parameters. Params controls the velocity and acceleration
        # Of the bullet. Arc determines the arc of the bullet, rotation controls the rotational offset
        # And spokes determines how many bullets are fired
        
        self.bulletxveliter = TimeIterator()
        self.bulletyveliter = TimeIterator()
        self.bulletxacciter = TimeIterator()
        self.bulletyacciter = TimeIterator()
        

        self.arcIter = TimeIterator()
        self.rotationIter = TimeIterator()
        self.spokes = 1
        self.angle = 0
        self.aimOffset = 0
        self.bullet_rules = [True, False, False, False, True]

        self.bulletHomingWeight = 0.01
        self.bulletHomingError = 0
        self.bulletHomingDelay = 0
        self.bullets_sticky_timer = 0
        
        # Spin rate measured in degrees per second
        self.spinRate = TimeIterator()

        # Is Targetting Tracks the player
        # Is Auto automatically fires at the target
        # Is Spinning automatically spins
        self.isTargetting = False
        self.isAuto = True
        self.isSpinning = False
        self.laserspinrate = 0
        self.waveradvel = 1
        self.waverad = 1
        self.wavearc = 360
        self.delay = 0

        # Modes: 0 -> Bullets, 1-> Lasers, 2 - > Waves
        self.mode = 0
        self.bulletorbitAcc = 0
        self.bulletorbitAngle = 0
        self.bulletorbitRad = 0
        self.bulletorbitRadAcc = 0
        self.bulletorbitRadVel = 0
        self.bulletOrbitTimer = -1
        self.bulletOrbitTimerStop = -1
        self.size = 5
        self.rules[4] = False
        self.fireWhenStop= False 
        self.fireWhenNotStop = False 
        
        # For "grenade" mode. Contains a list of shooters to fire. Each shooter gets deep copied so that there are bulletctr number of shooters
        self.shooterList = []

        # For random delays
        self.isRandomDelay = False
        self.mindelay = 0
        self.maxdelay = 0

        #Sync allows all fired shooters to fire simultaneously
        self.syncShooters = False
        self.mindelayShooters = 0
        self.maxdelayShooters = 0

        #If shooter symmetry is true, then each shooter (for mode 3 firing) will fire radially symmetric with respect to each
        #other. If not, then they will fire based on their specified target

        self.shooterSymmetry = True
        
        # Burst Size controls how many bullets are fired consecutively per shot.

        self.burstSize = 1
        self.burstDelay = 0 

        # Randomized fire determines whether or not a bullet is to be fired if automatic fire is disabled (i.e., the bullets
        # have a 1 / rof chance of spawning)
        self.randomTargettingmin = None
        self.randomTargettingmax = None
        self.isRandomTargetting = False

        self.bulletsLeftPerBurst = 1

        self.bulletctriter = TimeIterator()

        self.bullethometime = 100
        self.shooterdelay = 0

        # If momentum is set to true, then bullets that are no longer homing will change course and ignore bullet params 
        self.bulletHomingHomentum = False       

        # For sinusoidal bullets
        self.bulletsSinusoidal = False
        self.bulletsSinamp = 0
        self.bulletsSinFreq = 0


        # For adding edges
        self.hasEdges = False
        self.bulletsPerEdge = TimeIterator()
        self.vertices = []

    def setBulletsSinusoidal(self, amp = 1, freq = 1):
        self.bulletsSinusoidal = True
        self.bulletsSinamp = amp
        self.bulletsSinFreq = freq

    def setBulletCtrIter(self, rate, lowerbound = None, upperbound = None, oscillates = False, repeats = False):
        self.bulletctriter.rate = rate
        self.bulletctriter.oscillating = oscillates
        self.bulletctriter.repeating = repeats
        self.bulletctriter.lowerbound = lowerbound
        self.bulletctriter.upperbound = upperbound
    
    def setBulletArcIter(self, rate, lowerbound = None, upperbound = None, oscillates = False, repeats = False):
        self.arcIter.rate
        self.arcIter.oscillating = oscillates
        self.arcIter.repeating = repeats
        self.arcIter.lowerbound = lowerbound
        self.arcIter.upperbound = upperbound
    
    def setRandomTargetting(self, cond, minbound, maxbound):
        self.isRandomTargetting = val
        self.randomTargettingmin = minbound
        self.randomTargettingmax = maxbound

    def setBurstParams(self, burstsize, burstdelay):
        self.burstSize = burstsize
        self.burstDelay = burstdelay
        self.bulletsLeftPerBurst = burstsize

    def setFireWhenStop(self, val):
        self.fireWhenStop = val
    
    def setFireWhenNotStop(self, val):
        self.fireWhenNotStop = val

    def setShooterSymmetry(self, val):
        self.shooterSymmetry = val

    def setSync(self, mindelay, maxdelay):
        self.syncShooters = True
        self.mindelayShooters = mindelay
        self.maxdelayShooters = maxdelay

    def setDelayRange(self, mindelay, maxdelay):
        self.isRandomDelay = True
        self.mindelay = mindelay
        self.maxdelay = maxdelay

    def configRotationIter(self, minangle = None, maxangle = None, oscillating= False, repeating = False):
        self.rotationIter.lowerbound = math.radians(minangle)
        self.rotationIter.upperbound = math.radians(maxangle)
        self.rotationIter.oscillating = oscillating
        self.rotationIter.repeating = repeating

    def addShooter(self, shooter):
        self.shooterList.append(shooter)

    def setShooterColor(self, color):
        self.color = color

    def setShooterSize(self, size):
        self.size = size
    
    def setBulletsVisible(self, val):
        self.bullet_rules[4] = val

    def setBulletOrbitParams(self, vel, acc, rad, radvel = 0, radacc = 0, cond = True, orbitdelay = -1, orbitstop = -1):
        self.bulletorbitVel = math.radians(vel)
        self.bulletorbitAcc = math.radians(acc)
        self.bulletorbitRad = rad
        self.bulletorbitRadVel = radvel
        self.bulletorbitRadAcc = radacc
        self.bulletOrbitTimer = orbitdelay
        self.bulletOrbitTimerStop = orbitstop
        self.bullet_rules[3] = cond

    def setFiringDelay(self, delay):
        self.delay = delay

    def setWaveParams(self, rad, radvel, arc):
        self.waverad = rad
        self.waveradvel = radvel
        self.wavearc = arc
    
    def setBulletsStickyParams(self, stickytimer, stickytimerstop, cond = True):
        self.bullet_rules[2] = cond
        self.bullets_sticky_timer = stickytimer
        self.bullets_sticky_timer_stop = stickytimerstop

    def setMode(self, mode):
        self.mode = mode

    def setLaserSpinRate(self, val):
        self.laserspinrate = val

    def setBulletsHoming(self, val, delay = 0, timehoming = -1, weight = None, err = 0, momentum = False):
        self.bullet_rules[1] = val
        self.bullethometime = timehoming
        self.bulletHomingDelay = delay
        if weight != None:
            self.bulletHomingWeight = weight
        self.bulletHomingError = err
        self.bulletHomingHomentum = momentum 

    def setBulletSize(self, size):
        self.bullet_size = size

    def setSpinParams(self, spinrate, spinaccel = 0, spinratelowerbound = None, spinrateupperbound = None, spinrateOscillating = False, spinrateRepeating = False):
        self.spinRate.value = -1 * math.radians(spinrate)
        self.spinRate.rate = -1 * math.radians(spinaccel)
        if spinratelowerbound != None:
            self.spinRate.lowerbound = math.radians(spinratelowerbound)

        if spinrateupperbound != None:
            self.spinRate.upperbound = math.radians(spinrateupperbound)
        self.spinRate.oscillating = spinrateOscillating
        self.spinRate.repeating = spinrateRepeating
        self.isSpinning = True

    def setIsAuto(self, val):
        self.isAuto = val
        self.nextTime = self.birth + self.rof

    def setBulletsTargetting(self, cond, offset = 0, error = 0, weight = 1000 ):
        self.aimOffset = math.radians(offset)
        self.targettingError = error
        self.targettingWeight = weight
        self.isTargetting = cond

    def setInRadius(self, rad):
        self.inRadius = rad

    def setBulletsdeleteIfOut(self, val):
        self.bullet_rules[0]= val

    def setBullets(self, ctr):
        self.bulletctr =ctr

    def setAmmo(self, ctr):
        self.ammo = ctr

    def setBulletColor(self, color):
        self.bulletColor = color

    # setBulletLife sets the number of ticks before bullets are destroyed
    def setBulletLife(self, life):
        self.bulletlife = life

    # Motion simulates the movement of the shooter 

    def setROF(self, rof, rofrate = 0, roflbound = None, rofubound = None, rofOscillates = False, rofRepeats = False):
        self.rof = rof
        self.rofIter.value = rof

        if roflbound != None:
            self.rofIter.lowerbound = roflbound
        if rofubound != None:
            self.rofIter.upperbound = rofubound 

        self.rofIter.rate = rofrate
        self.rofIter.oscillating = rofOscillates
        self.rofIter.repeating = rofRepeats

    def setFiring(self, cond):
        self.firing = cond

    # setShape adjusts the shooter's arc, number of spokes and the rotational offset from 0 rad

    def setShape(self, arc , spokes, rotation, hasEdges = False, bulletsPerEdge = 0):

        self.arcIter.value =  math.radians(arc)
        self.rotationIter.value = -1 * math.radians(rotation) 

        if spokes == 1: 
            self.spokes = self.arcIter.value
        elif arc % 360 == 0:
            self.spokes = self.arcIter.value / (spokes)
        else:
            self.spokes = self.arcIter.value / (spokes - 1)   
        
        self.bulletctr = spokes

        self.hasEdges = hasEdges
        self.bulletsPerEdge.value = bulletsPerEdge


    # setBulletParams adjusts the x and y velocities and accelerations of bullets created by the object

    def setBulletParams(self, xv, yv, xa, ya):
        self.bulletxveliter.value = xv
        self.bulletyveliter.value = yv
        self.bulletxacciter.value = xa
        self.bulletyacciter.value = ya

    # Configure each paramiterator
    def configBulletxvel(self, rate = 0, lbound = None, ubound = None , oscillates = False, repeats = False):
        self.bulletxveliter.rate = rate
        
        if lbound != None:
            self.bulletxveliter.lowerbound = lbound

        if ubound != None:
            self.bulletxveliter.upperbound = ubound

        self.bulletxveliter.oscillating = oscillates
        self.bulletxveliter.repeating = repeats


    
    def configBulletyvel(self, rate = 0, lbound = None, ubound = None , oscillates = False, repeats = False):
        self.bulletyveliter.rate = rate
        
        if lbound != None:
            self.bulletyveliter.lowerbound = lbound

        if ubound != None:
            self.bulletyveliter.upperbound = ubound

        self.bulletyveliter.oscillating = oscillates
        self.bulletyveliter.repeating = repeats
    
    
    def configBulletxacc(self, rate = 0, lbound = None, ubound = None , oscillates = False, repeats = False):
        self.bulletxacciter.rate = rate
        
        if lbound != None:
            self.bulletxacciter.lowerbound = lbound

        if ubound != None:
            self.bulletyveliter.upperbound = ubound

        self.bulletxacciter.oscillating = oscillates
        self.bulletxacciter.repeating = repeats
    
    
    def configBulletyacc(self, rate = 0, lbound = None, ubound = None , oscillates = False, repeats = False):
        self.bulletyacciter.rate = rate
        
        if lbound != None:
            self.bulletyacciter.lowerbound = lbound

        if ubound != None:
            self.bulletyacciter.upperbound = ubound

        self.bulletyacciter.oscillating = oscillates
        self.bulletyacciter.repeating = repeats

    def configEdgeBullets(self, rate = 0, lbound = None, ubound = None , oscillates = False, repeats = False):
        self.bulletsPerEdge.rate = rate
        
        if lbound != None:
            self.bulletsPerEdge.lowerbound = lbound

        if ubound != None:
            self.bulletsPerEdge.upperbound = ubound

        self.bulletsPerEdge.oscillating = oscillates
        self.bulletsPerEdge.repeating = repeats



    # setAngle takes in angle as a parameter and sets that as the angle of tthe shooter

    def setAngle(self, angle):
        self.angle =(math.radians(360 -angle )) 

    # setTarget takes in the x and y coordinates of the target and uses that to calculate the angle

    def setTarget(self, dirx, diry):
        self.angle = getTarget(dirx, diry, self.xpos, self.ypos) 

    # Reload creates bullet objects
    def reload(self, time):
        size = self.bullet_size
        shooterdelay = 0
        self.rofIter.update()
        self.rof = self.rofIter.value


        # If the delay is to be random, change delay upon reload

        if self.isRandomDelay:
            self.delay = random.randrange(self.mindelay, self.maxdelay)
        if self.syncShooters:
            self.shooterdelay = random.randrange(self.mindelayShooters, self.maxdelayShooters)

        bulletno = int(self.bulletctr)
        # Add bullet objects
        if self.mode ==  0:
            for i in range(0, bulletno):
                b = Bullet()
                self.bullets.add(b)

        # Add laser objects
        elif self.mode == 1:
            for i in range(0, bulletno ):
                b = Laser()
                self.bullets.add(b)

        # Add wave objects
        elif self.mode == 2:
            for i in range(0, bulletno):
                b = Wave()
                self.bullets.add(b)


        #Add shooters
        elif self.mode == 3:
            for i in range(0, bulletno):
                for j in self.shooterList:
                    s = copy.deepcopy(j)
                    self.bullets.add(s)

        j = 0

        # Start with the vertices
        for obj in self.bullets:
            self.vertices.append(self.imbue(time, obj, j))
            j = j + 1

        if self.hasEdges and bulletno != 1:
            for v in range(0, len(self.vertices)):
                v1 = self.vertices[v]
                v2 = self.vertices[(v + 1) % len(self.vertices)]

                for e in range(0, self.bulletsPerEdge.value):
                    obj = None
                    if self.mode == 0:
                        obj = Bullet()
                    elif self.mode == 1:
                        obj = Laser()
                    elif self.mode == 2:
                        obj = Wave()
                    elif self.mode == 3:
                        for p in range(0, bulletno):
                            for q in self.shooterList:
                                obj = copy.deepcopy(q)
                                self.imbue(time, obj, e, v1 , v2)
                                self.bullets.add(obj)
                        continue
                    self.imbue(time, obj, e, v1 , v2)
                    self.bullets.add(obj)


        # Adjust for bullet spinning
        if self.isSpinning:
            self.spinRate.update()
            self.rotationIter.rate = self.spinRate.value
            
            self.rotationIter.update()
            if self.rotationIter.rate != self.spinRate.value:
                self.spinRate.value *= -1
        
        # Adjust the shape but only when within the boundaries 

        self.bulletctriter.value = 1
        
        if self.spokes != 0:
            self.bulletctriter.value = self.bulletctr

        self.bulletctriter.update()
        self.arcIter.update()
        self.setShape(math.degrees(self.arcIter.value), self.bulletctriter.value, -1 * math.degrees(self.rotationIter.value), self.hasEdges, self.bulletsPerEdge.value) 


        # Update velocity, acceleration, etc..
        self.bulletxveliter.update()
        self.bulletyveliter.update()
        self.bulletxacciter.update()
        self.bulletyacciter.update() 
        

    # Frees up space for next set of bullets

    def expend(self):
        for b in self.bullets:
            self.bullets.remove(b)
        self.vertices *= 0

    # Transfer properties to the object
    def imbue(self, time, obj, j, v1 =  None, v2 = None):

        edge = False
        expos = 0
        eypos = 0
        vectorx = 0
        vectory = 0
        eangle = 0

        if v1 != None and v2 != None:
            edge = True
            (x1, y1) = v1
            (x2, y2) = v2

            
            j += 1
            m = j
            n = self.bulletsPerEdge.value - j + 1
            expos = (m * x2 + n * x1) / (m + n)
            eypos = (m * y2 + n * y1) / (m + n)

            dx = expos - self.xpos
            dy = eypos - self.ypos
            rad = math.sqrt(dx * dx + dy * dy)

            vectorx = dx / rad
            vectory = dy / rad 

            eangle =(getTarget(dx, dy, 0, 0))


        bulletno = int(self.bulletctr)
        obj.setColor(self.bulletColor)

        obj.rules = self.bullet_rules

        a =  self.bulletxveliter.value
        b =  self.bulletyveliter.value
        c =  self.bulletxacciter.value
        d =  self.bulletyacciter.value

        isHoming = int(self.isTargetting) 

        # The following coeffs are used to ensure that the value of cosine and sine stay positive. 
        # These can be altered to produce other effects
        target = 0


        # Allows the Shooter to track movement
        if isHoming: 
            error = random.uniform(-1 * self.targettingError , 1 * self.targettingError)
            mousex, mousey = pygame.mouse.get_pos()
            target = getTarget(mousex, mousey, self.xpos, self.ypos) + math.radians(error) - self.arcIter.value / 2 + self.aimOffset


        # For Randomized Shooting
        elif self.isRandomTargetting:
            minimum = self.randomTargettingmin
            maximum = self.randomTargettingmax
            if self.randomTargettingmin == None:
                minimum = 0
            if self.randomTargettingmax== None:
                maximum = 360
            target = math.radians(random.randrange(minimum, maximum))
        
        xf = 0
        yf = 0
        x = 0
        y = 0
        if not edge:
            angle = j  * (self.spokes) +  self.rotationIter.value
            if bulletno == 1:
                angle = self.arcIter.value / 2 + self.rotationIter.value
            comp = j * (self.spokes) + target

            # Calculate the parameters (x and y pos, vel and acc ) of each bullet
            rfactor = self.targettingWeight *isHoming + 1
            if not self.isRandomTargetting:
                xf = (math.cos(angle + self.angle - self.arcIter.value / 2)  + self.targettingWeight * isHoming * math.cos(comp)) / rfactor
                yf = (math.sin(angle + self.angle - self.arcIter.value / 2) + self.targettingWeight *  isHoming *math.sin(comp)) / rfactor 
            else:
                xf = math.cos(comp)
                yf = math.sin(comp)

            x = self.xpos +  self.inRadius * xf
            y = self.ypos +  self.inRadius * yf

        l = 0
        if edge:
            x = expos
            y = eypos 
            xf = vectorx 
            yf = vectory
            v = math.sqrt(a * a + b * b)
            angle = eangle
            
            dx = self.xpos - x
            dy = self.ypos - y

            l = math.sqrt(dx * dx + dy * dy)

            a *= l / self.inRadius 
            b *= l / self.inRadius 
            c *= l / self.inRadius
            d *= l /self.inRadius

        xv = a * xf 
        yv = b * yf 
        xa = c * xf
        ya = d * yf
        
        obj.setParams(xv, yv, xa, ya)

        obj.angle = angle
        initialx = x
        initialy = y
            
        
        if self.bullet_rules[3]:
            if not edge:
                obj.setOrbitParams(self.bulletorbitVel, self.bulletorbitAcc, self.bulletorbitRad, x, y, angle)
                initialx = self.xpos + self.bulletorbitRad * math.cos(angle)
                initialy = self.ypos + self.bulletorbitRad * math.sin(angle)
                obj.setOrbitRadParams(self.bulletorbitRadVel, self.bulletorbitRadAcc)
            if edge:
                dist = l 
                obj.setOrbitParams(self.bulletorbitVel, self.bulletorbitAcc, dist , self.xpos, self.ypos, eangle)
                irad = self.bulletorbitRad
                obj.setOrbitRadParams(self.bulletorbitRadVel * l / irad, self.bulletorbitRadAcc * l / irad)
            obj.setOrbitTimer(self.bulletOrbitTimer)
            obj.setOrbitTimerStop(self.bulletOrbitTimerStop)
            obj.isOrbit = True
        
        obj.setLocation(x, y)

        obj.setLife(self.bulletlife)
        obj.setSize(self.bullet_size)
        obj.setBirth(time)
        obj.setFunctParams(self.bulletsSinusoidal, self.bulletsSinamp, self.bulletsSinFreq)
        
        
        # Adjust for homing parameters
        if self.bullet_rules[1]:
            obj.setHomingWeight(self.bulletHomingWeight)
            obj.setHomeTime(self.bullethometime)
            obj.setHomingError(self.bulletHomingError)
            obj.setHomingDelay(self.bulletHomingDelay)
            obj.setHomingMomentum(self.bulletHomingHomentum)

        # Adjust for sticky parameters
        if self.bullet_rules[2]:
            obj.setStickyTimer(self.bullets_sticky_timer)
            obj.setStickyTimerStop(self.bullets_sticky_timer_stop)

        # Adjust for laser parameters
        if self.mode == 1:
            obj.setAngle(angle + self.angle - self.arcIter.value / 2)
            obj.setLaserSpinRate(self.laserspinrate)

        # Adjust for wave parameters
        elif self.mode == 2:
            obj.setWaveParams(x, y, self.wavearc, self.waverad, self.waveradvel, self.rotationIter.value)
            obj.size = self.bullet_size

        elif self.mode == 3:
            if self.shooterSymmetry:
                obj.angle = angle
            else:
                (w, x, y, z) = obj.params
                obj.angle = getTarget(w, x ,0, 0)

            if obj.isRandomDelay and not self.syncShooters:
                obj.delay = random.randrange(obj.mindelay, obj.maxdelay)
            elif self.syncShooters:
                obj.delay = self.shooterdelay

        # Return the location of the vertex so it can be appended to the vertex list
        return (initialx, initialy)
