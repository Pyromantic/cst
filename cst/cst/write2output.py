# standard imports #

# adjust and write output to given #
class write2output (object):
    """adjust and write output, used by cStats sript"""
    
    # constructor #
    def __init__ (self) : 
        None

    ### variables ###

    outputFiles = []
    outputValue = []

    longest = 0

    ### methods ###
  
    # add file to output front
    def addFile (self, file) :
        self.outputFiles.append (file)
        
        if len(file) > self.longest :
            self.longest = len(file)

    # add value to output front
    def addValue (self, value) :
        self.outputValue.append (value)

    # write to given file
    def writeOutput (self, outFile, flag) :

        i = 0
        sum = 0

        for value in self.outputValue :
            sum += value

        self.addFile('CELKEM:')
        self.addValue(sum)

        for file in self.outputFiles :
            
            final = file

            length = len (file)

            while length < self.longest :
                final += ' '
                length += 1

            print (final , ' ' , self.outputValue[i])

            i += 1

