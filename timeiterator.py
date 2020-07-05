import math

class TimeIterator():
    def __init__(self):
        self.value = 0
        self.upperbound = None
        self.lowerbound = None
        self.oscillating = False
        self.repeating = False
        self.rate = 0

    def setOscillating(self, val):
        self.oscillating = val

    def setRepeating(self, val):
        self.repeating = val
    
    def get_value(self):
        return self.value

    def update(self):
        mincheck = checkLowerBound(self.lowerbound, self.value, self.rate)
        maxcheck = checkUpperBound(self.upperbound, self.value, self.rate)
        repeated = False

        if not mincheck or not maxcheck:
            if self.oscillating:
                self.rate = self.rate * -1
            elif self.repeating:
                self.value = repeatingSetter(self.upperbound, self.lowerbound, self.rate)
                repeated = True
            else:
                repeated = True

        if not repeated:
            self.value = self.value + self.rate

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