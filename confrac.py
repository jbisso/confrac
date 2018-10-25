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
        REPEATING = 1
        NON_REPEATING = 2
    
    precision = 100
    
    # ctor
    # kind[0] for finite, kind[1] for repeating | partialQuotients, refactor
    
    def __init__(self, cf, kind = Kind.FINITE):        
        if type(cf) is list:
            self.partialQuotients = cf
            self.kind = kind
        elif type(cf) is str:
            self._initFromString(cf)
        elif type(cf) is Fraction:
            self._initFromFraction(cf)
    
    def _initFromFraction(self, cf):
        self.kind = self.Kind.NON_REPEATING
        self.partialQuotients = []
        r = math.floor(cf)
        self.partialQuotients.append(r)
        for index in range(self.precision):
            i = math.floor(r)
            f = r - i
            if f == 0:
                self.kind = self.Kind.FINITE
                self.partialQuotients.append(i)
                break
            else:
                r = 1 / f
                self.partialQuotients.append(i)
         
    def _initFromString(self, cf):
        cf = cf.replace(' ', '')
        if cf[0] == '[' and cf[-1] == ']':
            partQuots = cf[1:-1].split(';')
            self.partialQuotients = int(partQuots[0])
            partQuots = partQuots[-1]
            if partQuots.endswith('...'):
                self.kind = self.Kind.FINITE
                partQuots = partQuots[:-3]
                if partQuots[0] == '(' and partQuots[-1] == ')':
                    self.kind = self.Kind.FINITE
                    self.partialQuotients = [int(d) for d in list(partQuots[1:-1])]
                else:
                    self.kind = self.Kind.REPEATING
                    self.partialQuotients = [int(d) for d in partQuots.split(',')]
            else:
                self.kind = self.Kind.FINITE
                self.partialQuotients = [int(d) for d in partQuots.split(',')]
    
    # generators for some interesting CF

    def _getRepetionGenerator(self, pattern, endPoint = 100):
        patternLength = len(pattern)
        while endPoint >= 0:
            yield pattern[endPoint % patternLength]
            endPoint -= 1
    
    @classmethod
    def getSquareRoot(cls, s):
        result = []
        rt = math.sqrt(s)
        if math.floor(rt) != rt:
            period, m, d, a = 0, 0, 1, math.floor(rt)
            result.append(a)
            for n in range(cls.precision):
                m = d * a - m
                d = math.floor( (s - m ** 2) / d )
                a = math.floor( (rt + m) / d )
                result.append(a)
                if a != 2 * result[0]:
                    period += 1
                else:
                    break
        return ContinuedFraction(result, kind = cls.Kind.REPEATING)

    def calculate(self):
        result = 0
        if self.kind == self.Kind.REPEATING:
            for b in self._getRepetionGenerator(self.partialQuotients[1:]):
                result = Fraction(1, b + result)
            result += self.partialQuotients[0]
        else:
            for b in self.partialQuotients[1:]:
                result = Fraction(1, b + result)
            result += self.partialQuotients[0]
        return result
        
    # [1; (2) ...] non-finite
    # [1; 1, 2, 3] finite

    def __str__(self):
        if self.kind == self.Kind.REPEATING:
            result = "[%s; (%s)" % (self.partialQuotients[0], "".join(str(e) for e in self.partialQuotients[1:]))
        else:
            result = "[%s; %s" % (self.partialQuotients[0], "".join(str(e) for e in self.partialQuotients[1:]))
        if self.kind == self.Kind.FINITE:
            result += "]"
        else:
            if self.kind == self.Kind.REPEATING:
                result += " ...]"
            else:
                result += "]"
        return result
    
def main():
    cf = ContinuedFraction.getSquareRoot(2)
    print("%s, %2.20f, %2.20f" % (cf, float(cf.calculate()), math.sqrt(2)))
    cf = ContinuedFraction(" [1; (2) ...]")
    print("%s, %2.20f, %2.20f" % (cf, float(cf.calculate()), math.sqrt(2)))
    cf = ContinuedFraction(" [2; 1, 2, 1, 1, 4, 1, 1, 6, 1 ...]")
    print("%s, %2.20f" % (cf, float(cf.calculate())))
    pat = " [12; 34, 1, 4]"    
    cf = ContinuedFraction(pat)
    print("%s, %2.20f" % (cf, float(cf.calculate())))
    pat = " [1; (121) ...]"    
    cf = ContinuedFraction(pat)
    print("%s, %2.20f" % (cf, float(cf.calculate())))
    pat = " [12; (5) ...]"    
    cf = ContinuedFraction(pat)
    print("%s, %2.20f" % (cf, float(cf.calculate())))
    pat = " [12; 34, 1, 4 ...]"    
    cf = ContinuedFraction(pat)
    print("%s, %2.20f" % (cf, float(cf.calculate())))

if __name__ == "__main__":
    main()
