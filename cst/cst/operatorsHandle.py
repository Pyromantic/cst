# standard imports #

# parse by operators #
class operators (object) :
    """ class handling operators and operations """
    # constructor #
    def __init__ (self) :
        None

    ### methods ###

    # dispatcher for known operands
    def dispatchOperands (self, char) :
        if not char :
            return False

        return { 
                '#' : lambda : operators._skip2EOL (self),
                '"' : lambda : operators._quotationHandle (self),
                '\'': lambda : operators._simpleQuotationHandle (self),
                '/' : lambda : operators._slashHandle (self),

                '-' : lambda : operators._minusLikeHandle (self),
                '+' : lambda : operators._plusLikeHandle (self), 

                '*' : lambda : operators._multiLikeHandle (self),

                '<' : lambda : operators._lesserLikeHandle (self),
                '>' : lambda : operators._greaterLikeHandle (self),

                '=' : lambda : operators._basicOperatorHandle (self, char),             
                '%' : lambda : operators._basicOperatorHandle (self, char),
                '&' : lambda : operators._basicOperatorHandle (self, char),
                '|' : lambda : operators._basicOperatorHandle (self, char),


                '^' : lambda : operators._XORhandle (self, char),

                '!' : lambda : operators._notHandle (self),

                '~' : lambda : operators._singleSpaceHandle (self),
                
          }[char]()

    # declaration block
    def declarator (self) :

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
               char = operators._declarationHandle (self)

        return self.fileFront.next()

    # checks if its in buffer a valid basic type
    def isDeclarator (self) :

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
   
    # operator slah handle
    def _slashHandle (self) : 
        char = self.fileFront.next()
            
        # single line commentary   
        if char == '/' :
            char = operators._skip2EOL (self)

        # multi line commentary
        elif char == '*' :
            char = operators._skip2EOC (self)
        
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

    # handles declaration block
    def _declarationHandle (self) :
        
        char = self.fileFront.next()
        while char != ';' and char != ',' :

            if char == '(' :
               char = operators._argumentsOperators (self)
               continue
            
            try :
               char = operators.dispatchOperands (self, char)
            except KeyError :
                char = self.fileFront.next()
                       
        return char

    # function arguments
    def _argumentsOperators (self) :
        char = self.fileFront.next()
        while char != ')':

            if char == '(' :
               char = operators._argumentsOperators (self)
               continue

            try :
                char = operators.dispatchOperands (self, char)
            except KeyError :
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
            if self.fileFront.data[self.fileFront._i - 2] == 'e' and operators._isExponencial (self) :
                return char

        else :
            if char == '+' or char == '=' :
                char = self.fileFront.next()

        self._operators += 1
 
        return char
    
    # HARD check if its double
    def _isExponencial (self) :
        if self.fileFront.data[self.fileFront._i - 3].isnumeric() :
            x = 4
            while self.fileFront.data[self.fileFront._i - x].isnumeric() or self.fileFront.data[self.fileFront._i - x] == '.' :
                x += 1

            if self.fileFront.data[self.fileFront._i - x].isspace() :
                return True
        
        return False


    #