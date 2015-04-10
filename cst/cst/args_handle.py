# standard imports #
import sys

 
# constants for args_handle class #
class _constants (object) :
    """constants for args_handle class"""

    @staticmethod
    def help () :
        return 'theres no help neither hope'

    @staticmethod
    def fewArgs () :
        return 'bylo zadano prilis malo argumentu'

    @staticmethod
    def manyArgs () :
        return 'bylo zadano prilis mnoho argumentu'

    @staticmethod
    def unknown () :
        return 'neznamy parametr '

    @staticmethod
    def unique () :
        return ' parametr nelze zadat vicekrat!' 

    @staticmethod
    def flags () :
        return ' o or i or k or c '

    @staticmethod
    def combine () :
         return ' parametr nelze kombinovat, ani zadat vicekrat!' 

    @staticmethod
    def requied () :
       return ' parametr je vyzadovan!'



# arguments handle class #
class args_handle (object) :
    """arguments parsing class, used by cStats script"""
    
    # consturctor
    def __init__ (self, argc, argv) :
        
        self._argcCheck (argc)

        self._parseArguments (argv)
       
        self._complete()

    # methods #

    # basic argument count check
    def _argcCheck (self, argc) : # checks argc

        if argc < 2 :
            raise AttributeError (_constants.fewArgs())

        if argc > 12 : 
            raise AttributeError (_constants.manyArgs())
    
    # arguments parsing
    def _parseArguments (self, argv) :  # parse arguments
        
        for arg in argv[1 :] :
   
            position = arg.find('=') 

            if 0 < position :

                 if  arg[0 : 2] == '--' :
                    self._setterDispatcher (arg[2 : position], arg[position + 1 :])
                 else :
                    self._setterDispatcher (arg[1 : position], arg[position + 1 :])

            else :

                if  arg[0 : 2] == '--' :
                    self._flagDispatcher (arg[2 :])   
                else :
                    self._flagDispatcher (arg[1 :])    

    # dispatcher for long arguments
    def _setterDispatcher (self, arg, value) : 
        try :
            {
            'input' : lambda value : self._inputSetter (value),
            'output': lambda value : self._outputSetter (value),
            'w'     : lambda value : self._parsingFlagSetter ('w_' + value),
            }[arg](value)
        except KeyError :
            self._unknownArgument (arg)
    
    # input file setter
    def _inputSetter (self, value) :
        if hasattr(self, '_input') :
            raise AttributeError ('input' + _constants.unique())
        else :
            self._input = value
    
    # reads standard input
    def _readInput (self) :
        None

    # output file setter
    def _outputSetter (self, value) :
        if hasattr(self, '_output') :
            raise AttributeError ('output' + _constants.unique())
        else :
            self._output = value

    # dispatcher for flags
    def _flagDispatcher (self, arg) : 
        try :
            {
            'o'         : lambda arg : self._parsingFlagSetter (arg),
            'i'         : lambda arg : self._parsingFlagSetter (arg),
            'k'         : lambda arg : self._parsingFlagSetter (arg),
            'c'         : lambda arg : self._parsingFlagSetter (arg),
            'p'         : lambda arg : self._pSetter(),
            'nosubdir'  : lambda arg : self._noSubDirFlag(),
            'help'      : lambda arg : self._helpPrinter(),
            }[arg](arg)
        except KeyError :
             self._unknownArgument (arg)
    
    # parsing flag setter
    def _parsingFlagSetter (self, flag) :
        if hasattr(self, '_parsingFlag') :
            raise AttributeError (flag, _constants.combine())

        self._parsingFlag = flag

    # p flag setter
    def _pFlag (self) :
        if hasattr(self, '_p') :
            raise AttributeError ('p' + _constants.unique())
        else :
            self._p = 1

    # no sub directory flag setter
    def _noSubDirFlag (self) :
        if hasattr(self, '_noSubDir') :
            raise AttributeError ('o' + _constants.unique())
        else :
            self._noSubDir = 1

    # help printer
    def _helpPrinter (self) :
        print(_constants.help())
        sys.exit(0)

    # unknown argument handler
    def _unknownArgument (self, arg) :
        raise AttributeError (_constants.unknown() + arg)

    # completes class
    def _complete (self) :

        if not hasattr(self, '_parsingFlag') :
            raise AttributeError (_constants.flags(), _constants.requied())

        if not hasattr(self, '_input') :
            self._readInput ()

        if not hasattr(self, '_noSubDir') :
            self._noSubDir = 0

        if not hasattr(self, 'p') :
            self._p = 0

        if not  hasattr(self, 'output') :
            self._output = 'stdout'