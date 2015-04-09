# standard imports #


# constants for fileParser class #
class _constants (object) :
    """constants for fileParser class"""

    @staticmethod
    def help () :
        return 'theres no help neither hope'

# file parser class #
class fileParser (object) :
    """file parsing class, used by cStats script"""

    # constructor 
    def __init__ (self, front, flag) :
        
        self.fileFront = front
    
        {
        'o' : lambda front : self._parseByOperators(front),
        'i' : lambda front : self._parseByIdentificators(front),
        'k' : lambda front : self._parseByKeywords(front),
        'c' : lambda front : self._parseByComments(front),
        'w' : lambda front : self._parseByPattern(front, flag),
        }[flag[0]](front)    
 
    # iterator
    def it (self) :
        if self._i < self._fileLength :
            self._i += 1
            return True
        else :
            return False

    # parse files by operators
    def _parseByOperators (self, front) :
        data2parse = self.fileFront._getFileContent()

        self._i = 0
        self._fileLength = len(data2parse) - 1

        data = lambda : data2parse[self._i] if self.it() else False

        self._operators = 0

        keyword = {'+' , '-', '*', '&', '!', '~', '=', '%', '<', '>', '|', '^', '.', '?'}

        char = data2parse[0]

        while char :
            try:
              char = { 
                '"' : lambda data : self._quotationHandle (data),
                '\'': lambda data : self._simpleQuotationHandle (data),
                '/' : lambda data : self._slashHandle (data),
                '+' : lambda data : self._plusHandle (data),
               
              }[char](data)
            except KeyError :
                char = data()          


    # operator slah handle
    def _slashHandle (self, data) : 
        char = data()
            
        # single line commentary   
        if char == '/' :
            char = self._skip2EOL (data)

        # multi line commentary
        elif char == '*' :
            char = self._skip2EOC (data)
        
        # probably operator
        else :
            self._operators += 1
        
        return char

    # skips till end of the line
    def _skip2EOL (self, data) :
        char = data()
        while char != '\n' and char :
            char = data()

        return char
    
    # skips till end of the multi line commentary
    def _skip2EOC (self, data) :
        char = data()

        while char :
              
            if char == '*' :
                char = data()
                if char == '/' :
                  return data()
            else :
                char = data()
  
    # quotation mark handle
    def _quotationHandle (self, data) :
        char = data()

        while char != '"' :
            char = data()
        
        return data()

    # simple quotation mark handle
    def _simpleQuotationHandle (self, data) :
        char = data()

        while char != '\'' :
            char = data()
        
        return data()

    # handles plus and associated operators
    def _plusHandle (self, data) :
        char = data()

        # probably increment or += operator
        if char == '+' or char == '=' :
            self._operators += 1
            char = data()

        # probably plus operator
        else :
            self._operators += 1

        return char