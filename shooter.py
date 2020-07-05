import random
import sys
import pygame
import math
import time
import copy
from bullet import *
from entities import * 
from patterns import * 
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
        self.bulletctr = 20
        self.firing = False
        self.bullets = pygame.sprite.Group()
        self.bulletlife = -1
        self.ammo = -1
        self.nextTime = 0 
        self.xvpattern = Pattern(0)
        self.yvpattern = Pattern(0)
        self.xapattern = Pattern(0)
        self.yapattern = Pattern(0)
        self.rofpattern = Pattern(0)
        self.spinpattern = Pattern(0)

        self.xvtpattern = Pattern(0)
        self.yvtpattern = Pattern(0)
        self.xatpattern = Pattern(0)
        self.yatpattern = Pattern(0)

        self.bullet_size = defualt_bullet_size
        self.bullets_sticky_timer_stop = -1

        # In radius determines the radius of a circle from which all bullets will start.
        # Out radius determines the point up to which all bullets will be deleted, - 1 indicates no outRadis
        self.inRadius = 0

        # Targetting weight determines how much targetting is prioritized
        # Targetting error determines how inaccurate the aim is

        self.targettingWeight = 1000
        self.targettingError = 0

        # Birth determines the time shooter is created
        self.birth = 0

        # The Following control Burst Shot Parameters. Params controls the velocity and acceleration
        # Of the bullet. Arc determines the arc of the bullet, rotation controls the rotational offset
        # And spokes determines how many bullets are fired
        
        self.params = (0, 0, 0, 0)
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
        self.spinRate = 0

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

        # For oscillations
        self.isOscillating = False

        # Repeating means that if the maxvalue has been reached, then set the value of the angle to be a predetermined value
        self.isRepeating = False

        self.minangle = None
        self.maxangle = None

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

    def setBulletCtrRepeating(self, val):
        self.bulletctriter.repeating = val

    def setBulletArcRepeating(self, val):
        self.arcIter.repeating = val

    def setIsRepeating(self, val):
        self.rotationIter.repeating = val

    def setRandomTargetting(self, val):
        self.isRandomTargetting = val

    # Set the range of angles to pick from
    def setRandomTargettingBounds(self, minimum, maximum):
        self.randomTargettingmin = minimum
        self.randomTargettingmax = maximum

    def setBulletCtrOscillates(self, val):
        self.bulletctriter.oscillating = val

    def setBulletArcOscillates(self, val):
        self.arcIter.oscillating = val

    def setBulletCtrBounds(self, minimum, maximum):
        self.bulletctriter.lowerbound = minimum
        self.bulletctriter.upperbound = maximum

    def setBulletArcBounds(self, minimum, maximum):
        self.arcIter.lowerbound = math.radians(minimum)
        self.arcIter.upperbound = math.radians(maximum)

    def setShapeCounters(self, bulletctrrate , bulletarcrate):
        self.bulletctriter.rate = bulletctrrate
        self.arcIter.rate = math.radians(bulletarcrate)

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

    def setIsOscillating(self, val):
        self.rotationIter.oscillating = val
        self.isSpinning = val

    # Min angle and Max Angle are in Degrees
    def setAngleBounds(self, minangle, maxangle):
        self.rotationIter.lowerbound = math.radians(minangle)
        self.rotationIter.upperbound = math.radians(maxangle)

    def addShooter(self, shooter):
        self.shooterList.append(shooter)

    def setShooterColor(self, color):
        self.color = color

    def setShooterSize(self, size):
        self.size = size
    
    def setBulletsVisible(self, val):
        self.bullet_rules[4] = val

    def setBulletsOrbit(self, cond):
        self.bullet_rules[3] = cond

    def setBulletOrbitParams(self, vel, acc, rad):
        self.bulletorbitVel = math.radians(vel)
        self.bulletorbitAcc = math.radians(acc)
        self.bulletorbitRad = rad

    def setBulletOrbitRadParams(self, vel, acc):
        self.bulletorbitRadVel = vel
        self.bulletorbitRadAcc = acc

    def setDelay(self, delay):
        self.delay = delay

    def setWaveRadius(self, rad):
        self.waverad = rad

    def setWaveRadVel(self, radvel):
        self.waveradvel = radvel

    def setWaveArc(self, arc):
        self.wavearc = arc
    
    def setBulletsSticky(self, val):
        self.bullet_rules[2] = val

    def setBulletsStickyTimer(self, val):
        self.bullets_sticky_timer = val

    def setBulletsStickyTimerStop(self, val):
        self.bullets_sticky_timer_stop = val

    def setMode(self, mode):
        self.mode = mode

    def setBulletHomingDelay(self, delay):
        self.bulletHomingDelay = delay

    def setBulletHomingWeight(self, weight):
        self.bulletHomingWeight = weight

    def setBulletHomingError(self, err):
        self.bulletHomingError = err

    def setLaserSpinRate(self, val):
        self.laserspinrate = val

    def setBulletsHoming(self, val):
        self.bullet_rules[1] = val

    def setBulletSize(self, size):
        self.bullet_size = size

    def setSpinPattern(self, ptrn):
        self.spinpattern = ptrn
        
    def setIsSpinning(self, val):
        self.isSpinning = val
    
    def getIsSpinning(self, val):
        return self.isSpinning

    def setSpinRate(self, spinrate):
        self.spinRate = -1 * math.radians(spinrate)

    def setIsAuto(self, val):
        self.isAuto = val
        self.nextTime = self.birth + self.rof

    def getIsAuto(self):
        return self.isAuto

    def setAimOffset(self, offset):
        self.aimOffset = math.radians(offset) 

    def setInRadius(self, rad):
        self.inRadius = rad

    def setTargettingError(self, val):
        self.targettingError = val

    def setTargettingWeight(self, val):
        self.targettingWeight = val 

    def setBulletsTargetting(self, val):
        self.isTargetting = val 
    
    def isShooterTargetting(self):
        return self.isTargetting

    def setBulletsdeleteIfOut(self, val):
        self.bullet_rules[0]= val

    def isBulletsdeleteIfOut(self):
        return self.bullet_rules[0]

    def setBullets(self, ctr):
        self.bulletctr =ctr

    def setBulletOrbitTimer(self, timer):
        self.bulletOrbitTimer = timer

    def setBulletOrbitTimerStop(self, timer):
        self.bulletOrbitTimerStop = timer

    # Create all patterns. Each param is a pattern

    def setxvelPattern(self, ptrn):
        self.xvpattern = ptrn
    def setyvelPattern(self, ptrn):
        self.yvpattern = ptrn
    def setxaccPattern(self, ptrn):
        self.xapattern = ptrn
    def setyaccPattern(self, ptrn):
        self.yapattern = ptrn

    def setxveltimePattern(self, ptrn):
        self.xvtpattern = ptrn
    def setyveltimePattern(self, ptrn):
        self.yvtpattern = ptrn
    def setxacctimePattern(self, ptrn):
        self.xatpattern = ptrn
    def setyacctimePattern(self, ptrn):
        self.yatpattern = ptrn


    def setrofPattern(self, ptrn):
        self.rofpattern = ptrn

    def setAmmo(self, ctr):
        self.ammo = ctr

    def setBulletColor(self, color):
        self.bulletColor = color

    # setBulletLife sets the number of ticks before bullets are destroyed
    def setBulletLife(self, life):
        self.bulletlife = life / 1000

    # Motion simulates the movement of the shooter 

    def setROF(self, rof):
        self.rof = rof

    def setFiring(self, cond):
        self.firing = cond

    # setShape adjusts the shooter's arc, number of spokes and the rotational offset from 0 rad

    def setShape(self, arc , spokes, rotation ):

        self.arcIter.value =  math.radians(arc)
        self.rotationIter.value = -1 * math.radians(rotation) 

        if spokes == 1: 
            self.spokes = self.arcIter.value
        elif arc % 360 == 0:
            self.spokes = self.arcIter.value / (spokes)
        else:
            self.spokes = self.arcIter.value / (spokes - 1)   
        
        self.bulletctr= int(spokes) 


    # setBulletParams adjusts the x and y velocities and accelerations of bullets created by the object

    def setBulletParams(self, xv, yv, xa, ya):
        self.params = (xv, yv, xa, ya)

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
        self.rof = self.rofpattern.eval(time / TIME_DECEL, self.rof)

        # If the delay is to be random, change delay upon reload

        if self.isRandomDelay:
            self.delay = random.randrange(self.mindelay, self.maxdelay)
        if self.syncShooters:
            shooterdelay = random.randrange(self.mindelayShooters, self.maxdelayShooters)

        # Add bullet objects
        if self.mode ==  0:
            for i in range(0, self.bulletctr):
                b = Bullet()
                self.bullets.add(b)

        # Add laser objects
        elif self.mode == 1:
            for i in range(0, self.bulletctr ):
                b = Laser()
                self.bullets.add(b)

        # Add wave objects
        elif self.mode == 2:
            for i in range(0, self.bulletctr):
                b = Wave()
                self.bullets.add(b)


        #Add shooters
        elif self.mode == 3:
            for i in range(0, self.bulletctr):
                for j in self.shooterList:
                    s = copy.deepcopy(j)
                    self.bullets.add(s)

        j = 0
        for obj in self.bullets:
            obj.setColor(self.bulletColor)

            obj.rules = self.bullet_rules

            (a, b, c, d) = self.params

            # Evaluate individual parameters using the pattern specified. If no pattern is specified return
            # The original value

            a =  (self.xvpattern.eval(time, a))
            b =  (self.yvpattern.eval(time, b))
            c =  (self.xapattern.eval(time, c))
            d =  (self.yapattern.eval(time, d))

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
    
            angle = j  * (self.spokes) +  self.rotationIter.value
            if self.bulletctr == 1:
                angle = self.arcIter.value / 2 + self.rotationIter.value
            comp = j * (self.spokes) + target

            # Calculate the parameters (x and y pos, vel and acc ) of each bullet
            rfactor = self.targettingWeight *isHoming + 1
            
            xf =0
            yf = 0
            if not self.isRandomTargetting:
                xf = (math.cos(angle + self.angle - self.arcIter.value / 2)  + self.targettingWeight * isHoming * math.cos(comp)) / rfactor
                yf = (math.sin(angle + self.angle - self.arcIter.value / 2) + self.targettingWeight *  isHoming *math.sin(comp)) / rfactor 
            else:
                xf = math.cos(comp)
                yf = math.sin(comp)

            x = self.xpos +  self.inRadius * xf
            y = self.ypos +  self.inRadius * yf
            

            xv = a * xf
            yv = b * yf
            xa = c * xf
            ya = d * yf
            
            obj.setParams(xv, yv, xa, ya)
            
            if self.bullet_rules[3]:
                obj.setOrbitParams(self.bulletorbitVel, self.bulletorbitAcc, self.bulletorbitRad, x, y, angle)
                obj.setOrbitRadParams(self.bulletorbitRadVel, self.bulletorbitRadAcc)
                obj.setOrbitTimer(self.bulletOrbitTimer)
                obj.setOrbitTimerStop(self.bulletOrbitTimerStop)
                obj.isOrbit = True
            
            obj.setLocation(x, y)

            obj.setLife(self.bulletlife)
            obj.setSize(self.bullet_size)
            obj.setBirth(time)
            
            
            # Adjust for homing parameters
            if self.bullet_rules[1]:
                obj.setHomingWeight(self.bulletHomingWeight)
                obj.setHomingError(self.bulletHomingError)
                obj.setHomingDelay(self.bulletHomingDelay)

            # Adjust for sticky parameters
            if self.bullet_rules[2]:
                obj.setStickyTimer(self.bullets_sticky_timer)
                obj.setStickyTimerStop(self.bullets_sticky_timer_stop)

            # Adjust for laser parameters
            if self.mode == 1:
                obj.setAngle(angle + self.angle - self.arc / 2)
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
                    obj.delay = shooterdelay

            j = j + 1
        
        # Adjust for bullet spinning

        if self.isSpinning:
            self.spinRate = math.radians(self.spinpattern.eval(time / TIME_DECEL, math.degrees(self.spinRate)))
            self.rotationIter.rate = self.spinRate
            
            self.rotationIter.update()
            self.spinRate = self.rotationIter.rate
        
        # Adjust the shape but only when within the boundaries 

        self.bulletctriter.value = 1
        
        if self.spokes != 0:
            self.bulletctriter.value = self.bulletctr

        self.bulletctriter.update()
        self.arcIter.update()
        self.setShape(math.degrees(self.arcIter.value), self.bulletctriter.value, -1 * math.degrees(self.rotationIter.value)) 
        

    # Frees up space for next set of bullets

    def expend(self):
        for b in self.bullets:
            self.bullets.remove(b)

def checkLowerBound(lbound, val, rate):
    if lbound == None:
        return True
    elif val + rate >= lbound:
        return True
    else:
        return False

def checkUpperBound(ubound, val, rate):
    if ubound == None:
        return True
    elif val + rate <= ubound:
        return True
    else:
        return False

def repeatingSetter(maxval, minval, rateval):
    if rateval >= 0:
        return minval
    else:
        return maxval