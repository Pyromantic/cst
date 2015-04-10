# standard imports #
import os

# constants for fileFront class #
class _constants (object) :
    """constants for fileFront class"""

    @staticmethod
    def notExists () :
        return ' soubor neexistuje'
    
    @staticmethod
    def combination () :
        return 'nelze kombinovat noSubDir a soubor'

# file front class #
class fileFront (object) :
    """class creating files front, used by cStats script"""

    # constructor #
    def __init__ (self, input, flag) :

        self.front = []

        if os.path.isdir(input) :
            self._fillUpFront (input, flag)

        elif os.path.isfile(input) :
            if flag :
               raise AttributeError (_constants.combination())
            
            self.front.append(input)

        else :
            raise AssertionError (input + _constants.notExists())

    ### variables ###
    _filePointer = -1
    _i = -1
    _fileLength = 0

    ### methods ###

    # sorts out given files into a front
    def _fillUpFront (self, input, flag) :

        if flag :
            
            path = input 
            if input[len(input) - 1] == '\\' :
                path = input[ : len(input) - 1] 

            files = [ f for f in os.listdir(input) if os.path.isfile(os.path.join(input,f)) ]
            
            for file in files:
                self._add2Front (path, file)
        else :
            for root, dir, files in os.walk(input) :
                for file in files:
                    self._add2Front (root, file)

    # add given file to the front
    def _add2Front (self, path, file) :
        try :
            {
            'c' : lambda : self.front.append(path + '\\' + file),
            'h' : lambda : self.front.append(path + '\\' + file),
            }[os.path.splitext(file)[1][1:]]()
        except KeyError :
            None

    # returns string containing file content
    def _getFileContent (self) :
        self._filePointer += 1 

        if self._filePointer >= len(self.front) :
            return False

        with open (self.front[self._filePointer]) as file:
            data = file.read()

        self._i = 0
        self._fileLength = len(data) - 1
        self.data = data

        return True

    # iterator
    def it (self) :
        if self._i < self._fileLength :
            self._i += 1
            return True
        else :
            return False

    next = lambda self : self.data[self._i] if self.it() else False

   

 

