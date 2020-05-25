import random
import sys
import math
import time
import pygame
import entities
import constants
from bullet import *
from shooter import *
from patterns import *
from presets import * 
from player import * 
from pygame.locals import DOUBLEBUF

# Initialize all constants

white = constants.white
black = constants.black
pi = math.pi
default_bullet_size = constants.default_bullet_size

# Create the Screen

SWIDTH = constants.SWIDTH
SHEIGHT = constants.SHEIGHT
OFFSET = constants.OFFSET

CURRENT_TIME = 0
pygame.init()
clock = pygame.time.Clock()
flags = DOUBLEBUF
screen = pygame.display.set_mode((SWIDTH, SHEIGHT), flags)
screen.set_alpha(None)
playarea = pygame.Surface((SWIDTH + OFFSET, SHEIGHT + OFFSET))
playarea.set_alpha(0)
playarea.fill(black)
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

fps = 60

# Initializing all entities

shooters = pygame.sprite.Group()
bulletsDisplayed = pygame.sprite.Group()
entitiesOffScreen = pygame.sprite.Group()
presetsList = pygame.sprite.Group()
player = Player()

# Initializing fonts: 
font = pygame.font.SysFont("Cambria Math", 20)

# Initializing events


# Update the FPS
def updatefps():
    fps = "FPS: " + str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, (0, 255, 0, 120))
    return fps_text

def showTime():
    time_elapsed =  "Time Elapsed: " + str(int(pygame.time.get_ticks() / 1000)) + "s"
    tim_text = font.render(time_elapsed, 1, (0, 255, 0 , 120))
    return tim_text

# Function to Draw the Bullets
def checkbounds(b, screen, SWIDTH, SHEIGHT):
    t = pygame.time.get_ticks() - b.birth
    if b.homingDelay <= t and b.rules[1] == True: 
        b.isHoming = True

    if b.stickyTimer <=t and b.rules[2] == True and b.stickyTimer != -1 and b.stickyTimerStop >= t and b.stickyTimerStop != -1:
        b.isSticky = True
    elif b.rules[2] and random.randrange(0, fps) == 1 and b.stickyTimer == -1: 
        b.isSticky = True
    else:
        b.isSticky = False

    if b.xpos - b.size > SWIDTH or b.ypos - b.size > SHEIGHT or b.xpos + b.size < 0 or b.ypos + b.size < 0:
        if b.isdeleteIfOut() == True:
            bulletsDisplayed.remove(b)
            del b
        else:
            entitiesOffScreen.add(b)
            bulletsDisplayed.remove(b)
    elif b.life == 0:
        bulletsDisplayed.remove(b)
        del b
    else: 
        b.draw(screen)
        if b.life != -1:
            b.life -= 1

# Function to add the bullets to displayedbullets array

def displayBullets():
    CURRENT_TIME = pygame.time.get_ticks()
    for s in shooters:
    # Condition to check whether or not to fire again
        if s.ammo == 0  or (CURRENT_TIME - s.birth ==s.life and s.life != -1 ):
            shooters.remove(s)
            del s
        elif random.randrange(0, fps) == 1 and not s.isAuto:
            s.reload(CURRENT_TIME)
            if s.ammo != -1:
                s.setAmmo(s.ammo - 1)
        elif s.nextTime - CURRENT_TIME <= 0 and s.isAuto:
            s.nextTime = CURRENT_TIME + s.rof
            s.reload(CURRENT_TIME)
            if s.ammo != -1:
                s.setAmmo(s.ammo - 1)
        
        try:
            for b in s.bullets:
                bulletsDisplayed.add(b)
            s.expend()
        except:
            continue

# Update bullets not on Screen
def updatebullets(b, screen , SWIDTH, SHEIGHT):

    if b.xpos - b.size > SWIDTH + OFFSET or b.ypos - b.size > SHEIGHT + OFFSET or b.xpos + b.size < - 1 * OFFSET or b.ypos + b.size < -1  * OFFSET:
        entitiesOffScreen.remove(b)
        del b
        return

    if b.xpos - b.size < SWIDTH or b.ypos - b.size < SHEIGHT or b.xpos + b.size > 0 or b.ypos + b.size > 0:
        bulletsDisplayed.add(b)
        entitiesOffScreen.remove(b)
        checkbounds(b, screen, SWIDTH, SHEIGHT) 

    if  pygame.time.get_ticks() - b.birth == b.life  and b.life != -1:
        entitiesOffScreen.remove(b)
        del b
    else: 
        b.draw(playarea)

# Draw and Motions

def main():
    pygame.init()
    def redraw():
        screen.fill(black)
        for b in bulletsDisplayed:
            checkbounds(b, screen, SWIDTH, SHEIGHT)
        for b in entitiesOffScreen:
            updatebullets(b, screen, SWIDTH, SHEIGHT)

        
        screen.blit(playarea, (0, 0))
        player.draw_Player(screen)

        # Debugging: 
        screen.blit(updatefps(), (10, 10))
        screen.blit(showTime(), (10, 25))


        pygame.display.update()

    while True:
        clock.tick(fps)
        CURRENT_TIME = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    p = Preset1()
                    p.setBirth(CURRENT_TIME)
                    presetsList.add(p)
                
                if event.key == pygame.K_a:
                    p = Preset2()
                    p.setBirth(CURRENT_TIME)
                    presetsList.add(p)

                if event.key == pygame.K_s:
                    p = Preset3()
                    p.setBirth(CURRENT_TIME)
                    presetsList.add(p)

                if event.key == pygame.K_SPACE:
                    p = Preset4()
                    p.setBirth(CURRENT_TIME)
                    presetsList.add(p)

                if event.key == pygame.K_f:
                    p = Preset5()
                    p.setBirth(CURRENT_TIME)
                    presetsList.add(p)

                if event.key == pygame.K_z:
                    p = Preset6()
                    p.setBirth(CURRENT_TIME)
                    presetsList.add(p)

                if event.key == pygame.K_x:
                    p = Preset7()
                    p.setBirth(CURRENT_TIME)
                    presetsList.add(p)

                if event.key == pygame.K_q:
                    p = Preset8()
                    p.setBirth(CURRENT_TIME)
                    presetsList.add(p)

        for p in presetsList:
            for s in p.shooter_list:
                shooters.add(s)
            del p

        mousex, mousey = pygame.mouse.get_pos()
        player.xpos = mousex
        player.ypos = mousey

        displayBullets()
        redraw()
        
    

main()

        
