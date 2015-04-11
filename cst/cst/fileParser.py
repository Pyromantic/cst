# standard imports #

# my imports #
from write2output       import write2output
from operatorsHandle    import operators

# constants for fileParser class #
class _constants (object) :
    """constants for fileParser class"""

    @staticmethod
    def help () :
        return 'theres no help neither hope'

# character buffer class #
class _characterBuffer (object) :
    """ buffer class, used by Cstats script """
    # constructor
    def __init__ (self) :
        None

    buffer = ''

    # adds character to buffer
    def add2Buffer (self, char) :
        if isinstance (char, str) :
            self.buffer += char

    # decides if buffer should be reseted
    def bufferReseter (self, next, char) :
        try:
           return {
                ';' : lambda : self.resetBuffer (next),
                ',' : lambda : self.resetBuffer (next),
                '(' : lambda : self.resetBuffer (next),
                ')' : lambda : self.resetBuffer (next),
                '\n': lambda : self.resetBuffer (next),
                '\t': lambda : self.resetBuffer (next),
                '\v': lambda : self.resetBuffer (next),
                }[char]()
        except KeyError :
            return char

    # resets buffer
    def resetBuffer (self, next) :
        self.buffer = ''
        return next()

# file parser class #
class fileParser (object) :
    """file parsing class, used by cStats script"""

    # constructor #
    def __init__ (self, front, flag) :
        
        self.fileFront = front
    
        {
        'o' : lambda : self._parseByOperators(front),
        'i' : lambda : self._parseByIdentificators(front),
        'k' : lambda : self._parseByKeywords(front),
        'c' : lambda : self._parseByComments(front),
        'w' : lambda : self._parseByPattern(front, flag),
        }[flag[0]]()    
 
    ### variables ###
    
    output = write2output()

    _buffer = _characterBuffer()
    _operators = 0

    ### methods ###

    # parse files by operators
    def _parseByOperators (self, front) :

        while self.fileFront._getFileContent() :
            
            self.output.addFile(self.fileFront.front[self.fileFront._filePointer])

            self._operators = 0

            char = self.fileFront.next()

            while char :

                char = self._buffer.bufferReseter (self.fileFront.next, char)

                try :
                    char = operators.dispatchOperands (self, char)
                except KeyError :
                    if char and not char.isspace() :

                        self._buffer.add2Buffer (char)

                        if operators.isDeclarator (self) :
                            char = operators.declarator (self)
                            continue

                    char = self.fileFront.next()         


            self.output.addValue (self._operators)
     