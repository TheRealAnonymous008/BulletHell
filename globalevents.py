
import random
import sys
import math
import time
import pygame
import entities
import constants
from bullet import *
from shooter import *
from presets import * 
from player import * 

class GlobalInit:
    def __init__(self):
        event_id = None
    

    # The function below is to be overrided by the user
    # Array contains all the bullets to be modified by the global event 
    def eventfunct(self, array = None):
        return