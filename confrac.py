from enum import Enum
from fractions import Fraction
import math
import sys

class ContinuedFraction():
    """
    Represents a finite or non-finite simple continued fraction.
    The constructor takes any Fraction, list, or a string (notation).
    """
    
    class Kind(Enum):
        FINITE = 0
        NON_FINITE = 1 # actually non-finite non-repeating
        REPEATING = 2 # actually non-finite, repeating
    
    precision = 100
    
    # generators for some interesting CF

    def _getRepetionGenerator(self, endPoint = 100):
        patternLength = len(self.partialQuotients[1:])
        while endPoint > 0:
            print(self.partialQuotients[1:], self.partialQuotients[1:][endPoint % patternLength])
            yield self.partialQuotients[1:][endPoint % patternLength]
            endPoint -= 1
            
    def _getNextNumberGenerator(self, endPoint = 100):
        patternLength = len(self.partialQuotients[1:])
        if endPoint < patternLength:
            i = endPoint
        else:
            i = patternLength
        while i > 0:
            yield self.partialQuotients[1:][i]
            i -= 1
    
    def __init__(self, cf, kind = Kind.FINITE, genFunc = None):
        """
        Creates an object from a simple list, string of the older notation,
        or a Fraction. genFunc provides a generator for the sequence.
        """
        if type(cf) is list:
            self.partialQuotients = cf
            self.kind = kind
        elif type(cf) is str:
            self._initFromString(cf)
        elif type(cf) is Fraction:
            self._initFromFraction(cf)
        else:
            raise TypeError('type of cf argument must be a list, string, or Fraction!')
        if genFunc:
            #print(genFunc, type(genFunc))
            self.genFunc = genFunc
    
    def _initFromFraction(self, cf):
        """All CFs from ratios (Fraction) are finite."""
        
        self.kind = self.Kind.FINITE
        self.genFunc = ContinuedFraction._getNextNumberGenerator
        self.partialQuotients = []
        r = math.floor(cf)
        self.partialQuotients.append(r)
        for index in range(self.precision):
            i = math.floor(r)
            f = r - i
            if f == 0:
                self.partialQuotients.append(i)
                break
            else:
                r = 1 / f
                self.partialQuotients.append(i)
         
    def _initFromString(self, cf):
        cf = cf.replace(' ', '')
        if cf[0] == '[' and cf[-1] == ']':
            partQuots = cf[1:-1].split(';')
            self.partialQuotients = [int(partQuots[0])]
            partQuots = partQuots[-1]
            if partQuots.endswith('...'):
                partQuots = partQuots[:-3]
                if partQuots[0] == '(' and partQuots[-1] == ')':
                    self.kind = self.Kind.REPEATING
                    self.genFunc = ContinuedFraction._getNextNumberGenerator
                    self.partialQuotients = self.partialQuotients + [int(d) for d in partQuots[1:-1].split(',')]
                else:
                    self.kind = self.Kind.NON_FINITE
                    self.genFunc = ContinuedFraction._getNextNumberGenerator
                    self.partialQuotients = self.partialQuotients + [int(d) for d in partQuots.split(',')]
            else:
                self.kind = self.Kind.FINITE
                self.genFunc = ContinuedFraction._getNextNumberGenerator
                self.partialQuotients = self.partialQuotients + [int(d) for d in partQuots.split(',')]
    
    @classmethod
    def getSquareRoot(cls, s):
        result = []
        rt = math.sqrt(s)
        if math.floor(rt) != rt:
            m, d, a = 0, 1, math.floor(rt)
            result.append(a)
            for n in range(cls.precision):
                m = d * a - m
                d = math.floor( (s - m ** 2) / d )
                a = math.floor( (rt + m) / d )
                result.append(a)
                if a == 2 * result[0]:
                    break
        return ContinuedFraction(result, kind = cls.Kind.REPEATING, genFunc = cls._getRepetionGenerator)

    def calculate(self):
        result = 0
        if self.kind == self.Kind.REPEATING:
            for b in self.genFunc(self):
                print("b:", b, "result: ", result )
                result = Fraction(1, b + result)
            result += self.partialQuotients[0]
        else:
            for b in reversed(self.partialQuotients[1:]):
                result = Fraction(1, b + result)
            result += self.partialQuotients[0]
        return result
        
    # [1; (2, 4) ...] non-finite
    # [1; 1, 2, 3] finite

    def __str__(self):
        if self.kind == self.Kind.REPEATING:
            if len(self.partialQuotients[1:]) > 1:
                tmp = "".join([str(e) + ', ' for e in self.partialQuotients[1:]]) + str(self.partialQuotients[-1])
            else:
                tmp = str(self.partialQuotients[1])
            #print("_str() %s %s %s" % (self.partialQuotients[1:], self.partialQuotients[-2], self.partialQuotients), tmp)
            result = "[%s; (%s)" % (self.partialQuotients[0], tmp)
        else:
            result = "[%s; %s" % (self.partialQuotients[0], str(self.partialQuotients[1:])[1:-1])
        if self.kind == self.Kind.FINITE:
            result += "]"
        else:
            if self.kind == self.Kind.REPEATING:
                result += " ...]"
            else:
                result += "]"
        return result

def testPrint(cf, extra = None):
    if extra:
        print("%s, %2.20f, %2.20f" % (cf, float(cf.calculate()), extra))
    else:
        print("%s, %2.20f" % (cf, float(cf.calculate())))

def main():
    #testPrint(ContinuedFraction.getSquareRoot(2), math.sqrt(2))
    cf = ContinuedFraction(" [1; (2) ...]")
    print("cf, cf.partialQuotients, cf.partialQuotients[1:]", cf, cf.partialQuotients, cf.partialQuotients[1:])
    testPrint(cf)
    testPrint(ContinuedFraction.getSquareRoot(3), math.sqrt(3))
    testPrint(ContinuedFraction.getSquareRoot(23), math.sqrt(23))
    testPrint(ContinuedFraction(" [1; (2, 4, 5) ...]"))
    testPrint(ContinuedFraction("[2; 1, 2, 1, 1, 4, 1, 1, 6, 1 ...]"))
    testPrint(ContinuedFraction("[12; 34, 1, 4 ...]"))
    testPrint(ContinuedFraction("[2; 1, 2, 1, 1, 4, 1, 1, 6, 1 ...]"), math.e)
    testPrint(ContinuedFraction("[12; (5) ...] "))
    testPrint(ContinuedFraction(" [12; 34, 1, 4]"), 12.028735632183908)
    testPrint(ContinuedFraction("[3; 4, 12, 4]" ), 3.245)
    testPrint(ContinuedFraction("[0; 1, 5, 2, 2]"))
    testPrint(ContinuedFraction("[3; 7, 15, 2, 7, 1, 4, 2]"), 3.14155)
    #cf = ContinuedFraction(3.1415)
    cf = ContinuedFraction("[1; (2) ...]", genFunc = ContinuedFraction._getRepetionGenerator)
    
if __name__ == "__main__":
    main()
