# Contains all necessary constants

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)

default_bullet_size = 3
SWIDTH =  800
SHEIGHT = 600  
OFFSET = 200
TIME_DECEL = 1000
FPS = 60

BUFFERCTR = 0
LASTBUFFER = 0

def updateBufferCtr(val):
    BUFFERCTR = val 

def updateLastBuffer(val):
    LASTBUFFER = val