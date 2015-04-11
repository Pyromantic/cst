# standard imports #

# my imports #
from write2output import write2output

# constants for fileParser class #
class _constants (object) :
    """constants for fileParser class"""

    @staticmethod
    def help () :
        return 'theres no help neither hope'

# character buffer class
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

    # dispatcher for known operands
    def _dispatchOperands (self, char) :
        if not char :
            return False

        return { 
                '#' : lambda : self._skip2EOL(),
                '"' : lambda : self._quotationHandle (),
                '\'': lambda : self._simpleQuotationHandle (),
                '/' : lambda : self._slashHandle (),

                '-' : lambda : self._minusLikeHandle (),
                '+' : lambda : self._plusLikeHandle (),  

                '*' : lambda : self._multiLikeHandle (),

                '<' : lambda : self._lesserLikeHandle (),
                '>' : lambda : self._greaterLikeHandle (),

                '=' : lambda : self._basicOperatorHandle (char),             
                '%' : lambda : self._basicOperatorHandle (char),
                '&' : lambda : self._basicOperatorHandle (char),
                '|' : lambda : self._basicOperatorHandle (char),


                '^' : lambda : self._XORhandle(char),

                '!' : lambda : self._notHandle (),

                '~' : lambda : self._singleSpaceHandle (),
                
          }[char]()
    
    # parse files by operators
    def _parseByOperators (self, front) :

        while self.fileFront._getFileContent() :
            
            self.output.addFile(self.fileFront.front[self.fileFront._filePointer])

            self._operators = 0

            char = self.fileFront.next()

            while char :

                char = self._buffer.bufferReseter (self.fileFront.next, char)

                try :
                    char = self._dispatchOperands (char)
                except KeyError :
                    if char and not char.isspace() :

                        self._buffer.add2Buffer (char)

                        if self._isDeclarator () :
                            char = self._declarator ()
                            continue

                    char = self.fileFront.next()         


            self.output.addValue (self._operators)
     
    # checks if its in buffer a valid basic type
    def _isDeclarator (self) :

        declarator = lambda str : True if str and (str.isspace() or str == '*') else False

        try : 
            declarator = {
                'void'  : lambda : declarator(self.fileFront.next()),
                'int'   : lambda : declarator(self.fileFront.next()),
                'char'  : lambda : declarator(self.fileFront.next()),
                'short' : lambda : declarator(self.fileFront.next()),
                'float' : lambda : declarator(self.fileFront.next()),
                'double': lambda : declarator(self.fileFront.next()),
                'long'  : lambda : declarator(self.fileFront.next()),
            }[self._buffer.buffer]()
        except KeyError :
            declarator = False
        
        return declarator
   
    # handles declaration block
    def _declarationHandle (self) :
        
        char = self.fileFront.next()
        while char != ';' and char != ',' :

            if char == '(' :
               char = self._argumentsOperators ()
               continue
            
            try :
               char = self._dispatchOperands (char)
            except KeyError :
                char = self.fileFront.next()
                       
        return char

    # function arguments
    def _argumentsOperators (self) :
        char = self.fileFront.next()
        while char != ')':

            if char == '(' :
               char = self._argumentsOperators (self)
               continue

            try :
                char = self._dispatchOperands (char)
            except KeyError :
                char = self.fileFront.next()
                       
        return self.fileFront.next()

    # declaration block
    def _declarator (self) :

        char = self._buffer.resetBuffer (self.fileFront.next)

        while char != False :
            try :
                char = {
                ';' : lambda : False,
                '{' : lambda : False,

                '=' : lambda : True,
                }[char]()
            except KeyError :
                char = self.fileFront.next()
                continue

            if char == True :
               self._operators += 1
               char = self._declarationHandle ()

        return self.fileFront.next()

    # operator slah handle
    def _slashHandle (self) : 
        char = self.fileFront.next()
            
        # single line commentary   
        if char == '/' :
            char = self._skip2EOL ()

        # multi line commentary
        elif char == '*' :
            char = self._skip2EOC ()
        
        # probably operator
        else :
            self._operators += 1
        
        return char

    # skips till end of the line
    def _skip2EOL (self) :
        char = self.fileFront.next()
        while char != '\n' and char :
            char = self.fileFront.next()

        return self.fileFront.next()
    
    # skips till end of the multi line commentary
    def _skip2EOC (self) :
        char = self.fileFront.next()

        while char :        
            if char == '*' :
                char = self.fileFront.next()
                if char == '/' :
                  return self.fileFront.next()
            else :
                char = self.fileFront.next()
  
    # quotation mark handle
    def _quotationHandle (self) :
        char = self.fileFront.next()

        while char != '"' :
            if char == '\\' :
                self.fileFront.next()
            char = self.fileFront.next()

        return self.fileFront.next()

    # simple quotation mark handle
    def _simpleQuotationHandle (self) :
        char = self.fileFront.next()

        while char != '\'' :
            if char == '\\' :
                self.fileFront.next()
            char = self.fileFront.next()
        
        return self.fileFront.next()

    # handles given operator and associated operators
    def _basicOperatorHandle (self, operator) :
        char = self.fileFront.next()

        # probably increment/decrement/multidimensional or overloaded = operator
        if char == operator or char == '=' :
            char = self.fileFront.next()

        # else  probably just simple operator
        self._operators += 1


        return char

    # handle XOR operator
    def _XORhandle (self) :
        char = self.fileFront.next()

        if char == '=' :
            self.fileFront.next()

        self._operators += 1


        return self.fileFront.next()

    # single space operators handle
    def _singleSpaceHandle (self) :
        self._operators += 1
        return self.fileFront.next()
    
    # not operator handle
    def _notHandle (self) :
        char = self.fileFront.next()

        if char == '=' : 
            self.fileFront.next()
        
        self._operators += 1

        return self.fileFront.next()

    # handles minus and associated operators (look-a-like)
    def _minusLikeHandle (self) :
        char = self.fileFront.next()

        if char.isnumeric() : 
            if self.fileFront.data[self.fileFront._i - 2] == 'e' and self._isDouble() :
                return char

        #  -> operator or -- operator or == operator #
        if char == '>' or char == '-' or char == '=' :
           char = self.fileFront.next()

        # increments operators
        self._operators += 1

        return char

    # handles plus and associated operatorrs (look-a-like)
    def _plusLikeHandle (self) :
        char = self.fileFront.next()

        # funny part
        if char.isnumeric() : 
            if self.fileFront.data[self.fileFront._i - 2] == 'e' and self._isDouble() :
                return char

        else :
            if char == '+' or char == '=' :
                char = self.fileFront.next()

        self._operators += 1
 
        return char
    
    # HARD check if its double
    def _isDouble (self) :
        if self.fileFront.data[self.fileFront._i - 3].isnumeric() :
            x = 4
            while self.fileFront.data[self.fileFront._i - x].isnumeric() or self.fileFront.data[self.fileFront._i - x] == '.' :
                x += 1

            if self.fileFront.data[self.fileFront._i - x].isspace() :
                return True
        
        return False

    # handles lesser and associated operators (look-a-like)
    def _lesserLikeHandle (self) :
        char = self.fileFront.next()

        self._operators += 1

        if char == '<' :
            char = self.fileFront.next()

            if char == '=' :               
                return self.fileFront.next()
            else :
                return char

        elif char == '=' :
           return self.fileFront.next()

        else : 
           return char
    
    # handles greater and associated operators (look-a-like)
    def _greaterLikeHandle (self) :
        char = self.fileFront.next()

        self._operators += 1

        if char == '>' :
            char = self.fileFront.next()

            if char == '=' :               
                return self.fileFront.next()
            else :
                return char

        elif char == '=' :
           return self.fileFront.next()

        else : 
           return char

    # handles multiplication and associated operators (look-a-like)
    def _multiLikeHandle (self) :
        char = self.fileFront.next()
        self._operators += 1

        if char == '=' :
            return self.fileFront.next()

        while char == '*' :
            self._operators += 1
            char = self.fileFront.next()

        return char

    #