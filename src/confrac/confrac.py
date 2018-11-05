from enum import Enum
from fractions import Fraction
import math
import sys

class ContinuedFraction():
    class Kind(Enum):
        F = 0
        NFR = 1
        NFNR = 2
        
    precision = 100
    
    # generators    
    def _repetionGenerator(self, endPoint = precision):
        patternLength = len(self.rest)
        while endPoint >= 0:
            yield self.rest[endPoint % patternLength]
            endPoint -= 1
            
    def _nextNumberGenerator(self, endPoint = precision):
        patternLength = len(self.rest)
        if endPoint < patternLength:
            index = endPoint
        else:
            index = patternLength
        while index > 0:
            yield self.rest[index % patternLength]
            index -= 1

    # ctor
    def __init__(self, partialQuotients = [0], kind = Kind.F):
        """
        Creates an object from a simple list, string of the older notation,
        or a Fraction. genFunc provides a generator for the sequence.
        """
        
        self.kind = kind
        if type(partialQuotients) is list:
            self._partialQuotients = partialQuotients
        elif type(partialQuotients) is str:
            self._initFromString(partialQuotients)
        elif type(partialQuotients) is Fraction:
            self._initFromFraction(partialQuotients)
        else:
            raise TypeError('type of cf argument must be a list, string, or Fraction!')
    
    def _initFromFraction(self, cf):
        """All CFs from ratios (Fraction) are finite."""
        
        self.kind = self.Kind.F
        self._partialQuotients = []
        r = math.floor(cf)
        self._partialQuotients.append(r)
        for index in range(self.precision):
            i = math.floor(r)
            f = r - i
            if f == 0:
                self._partialQuotients.append(i)
                break
            else:
                r = 1 / f
                self._partialQuotients.append(i)
         
    def _initFromString(self, cf):
        cf = cf.replace(' ', '')
        if cf[0] == '[' and cf[-1] == ']':
            partQuots = cf[1:-1].split(';')
            self._partialQuotients = [int(partQuots[0])]
            partQuots = partQuots[-1]
            if partQuots.endswith('...'):
                partQuots = partQuots[:-3]
                if partQuots[0] == '(' and partQuots[-1] == ')':
                    self.kind = self.Kind.NFR
                    self._partialQuotients = self._partialQuotients + [int(d) for d in partQuots[2:-2].split(',')]
                else:
                    self.kind = self.Kind.NFNR
                    self._partialQuotients = self._partialQuotients + [int(d) for d in partQuots.split(',')]
            else:
                self.kind = self.Kind.F
                self._partialQuotients = self._partialQuotients + [int(d) for d in partQuots.split(',')]

    @property
    def a0(self):
        return self._partialQuotients[0]
        
    @property
    def rest(self):
        return self._partialQuotients[1:]
        
    def calculate(self, terms = precision):
        result = 0
        if self.kind == self.Kind.NFR:
            for b in self._repetionGenerator(terms):
                result = Fraction(1, b + result)
            result += self.a0
        elif self.kind == self.Kind.F:
            for b in self._nextNumberGenerator(terms):
                result = Fraction(1, b + result)
            result += self.a0
        return result
        
    # [1; ([2, 4]) ...] non-finite, repeating
    # [1; 1, 2, 3] finite

    def __str__(self):
        if self.kind == self.Kind.NFR:
            if len(self.rest) > 1:
                tmp = "".join([str(e) + ', ' for e in self.rest])
                tmp = "[" + tmp[:-2] + "]"
            else:
                tmp = str(self.rest)
            result = "[%s; (%s)" % (self.a0, tmp)
        else:
            result = "[%s; %s" % (self.a0, str(self.rest)[1:-1])
        if self.kind == self.Kind.F:
            result += "]"
        else:
            if self.kind == self.Kind.NFR:
                result += " ...]"
            else:
                result += "]"
        return result
        
    @classmethod
    def getSquareRoot(cls, s):
        """All square roots of non-perfect squares are non-finite, repeating CFs."""
        
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
        return ContinuedFraction(result, kind = cls.Kind.NFR)

def main():
    print("Testing")
    cf = ContinuedFraction("[1; ([2]) ...]")
    print(cf, cf.a0, cf.rest, cf.calculate())
    cf = ContinuedFraction([1, 2], ContinuedFraction.Kind.NFR)
    print(cf, cf.a0, cf.rest, cf.calculate())
    cf = ContinuedFraction([3, 2])
    print(cf, cf.a0, cf.rest, cf.calculate())
    cf = ContinuedFraction("[3; 2, 1, 3]")
    print(cf, cf.a0, cf.rest, cf.calculate())

if __name__ == "__main__":
    main()

