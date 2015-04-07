# standard imports #
import sys

# my imports #
from args_handle import args_handle # arguments handle
from fileFront   import fileFront   # creates file front
from fileParser  import fileParser  # file parser

# main class #
class cStats (object) :
    """ program C stats, use help for more informations """

    # constructor
    def __init__ (self, argc, argv) :

        # arguments handle
        arguments = args_handle (argc, argv)
        
        # files front
        front = fileFront (arguments._input, arguments._noSubDir)

        # file parser
        parser = fileParser (front, arguments._parsingFlag)
        


# executes main, runs script
if __name__ == "__main__" :
    try :
        cStats (len(sys.argv), sys.argv)
    except AttributeError as err :
        print (err)  
    except AssertionError as err :
        print (err)

else :  # do nothing
    None
