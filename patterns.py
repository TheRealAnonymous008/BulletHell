import math
import enum

# The following class controls the velocity and acceleration of each bullet
# Pattern types: 
# 0 -> No Pattern, simply returns what is argued
# 1 -> Polynomial, returns P(t) + x. Arguments are of decreasing degree, i.e. [3, 2, 1] corresponds to
#      3t^2 + 2t + 1
# 2 -> Sine, takes  in the first four parameters and evaluates A sin (Bx - C) + D
# 3 -> Cosine, takes in the first four parameters and evaluates A cos (Bx - C) + D


# For bounded, the following are the values:
# Bound Mode takes in a number 0  -> none, 1 -> exclusive, 2 - > inclusive

class Pattern:
    def __init__(self, ptype):
        self.ptype = ptype
        self.params = []
        self.lowerbound = 0
        self.upperbound = 0
        self.lbounded = 0
        self.ubounded = 0

    def setBoundedMode(self, lmode, umode):
        self.lbounded = lmode
        self.ubounded = umode

    def setUpperBound(self, bound):
        self.upperbound = bound
    
    def setLowerBound(self, bound):
        self.lowerbound = bound

    def setParams(self, params):
        self.params = params

    # Eval evaulates the function using specified parameters. t represents the time and x represents the 
    # initial conditions

    def eval(self, t, x):
        result = 1
        
        if self.ptype == 0:
            result = x

        elif self.ptype == 1:
            result = 0
            for i in self.params:
                result = i + result * t
            result = result + x

        elif self.ptype == 2:
            result = 0
            
            while len(self.params) < 4:
                self.params.append(0)

            a = self.params[0]
            b = self.params[1]
            c = self.params[2]
            d = self.params[3]

            x = math.radians(x)
            result = x + a *  math.sin(math.radians(b * t + c)) + d

        elif self.ptype == 3:
            result = 0
            
            while len(self.params) < 4:
                self.params.append(0)

            a = self.params[0]
            b = self.params[1]
            c = self.params[2]
            d = self.params[3]

            x = math.radians(x)

            result = x +  a * math.cos(math.radians(b * t + c)) + d

        isbelowupper = False
        isabovelower = False

        if self.ubounded == 1 and self.upperbound > result:
            isbelowupper = True
        elif self.ubounded == 2 and self.upperbound >= result:
            isbelowupper = True
        elif self.ubounded == 0:
            isbelowupper = True
        else:
            isbelowupper = False

        if self.lbounded == 1 and self.lowerbound < result:
            isabovelower = True
        elif self.lbounded == 2 and self.lowerbound <= result:
            isabovelower = True
        elif self.lbounded ==0 :
            isabovelower = True
        else:
            isabovelower = False

        if isbelowupper and isabovelower: 
            return result 
        elif isbelowupper and not isabovelower: 
            return self.lowerbound
        elif not isbelowupper and isabovelower:
            return self.upperbound
    
