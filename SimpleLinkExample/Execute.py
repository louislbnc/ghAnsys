"""This component takes an Ansys file input as a strign, bottles it up
and starts Ansys to run the simulation

    Inputs:
        installLocation: provide your installation location for Ansys
        likely to look like: C:\Program Files\ANSYS Inc\ANSYS Student\v191\ansys\bin\winx64\ANSYS191
        In your file explorer, that file will actually have the extension .exe but don't include it.
        
        
        workFolder: provide a disk location where you want to start the program from. All files will 
        be written to this folder
        
        ansysFileStrings: provide your full Ansys input as a multiline string that's in a single
        Grasshopper item
        
        run: boolean toggle to start the simulation
        
    Outputs:
        These are files we're creating in our Ansys input file. Keep in mind 
        you could easily add your own files here. Just add them to the
        writeBatchFile function.
        
        nodeFile: Folder location for the nodal solutions
        nodeFile: Folder location for the elemental solutions
        
"""
        
__author__ = "Louis Leblanc"
__version__ = "2018.11.05"
        
import os
        
###Function Definitions

#Write out the Ansys input file we've wrote out in the previous Python component
def writeInputFile(folderLocation, ansysInputFile):
    f = open( (workFolder+'\ghAnsysInput.txt'),'w') #make a string from the work folder + the name we give to the input file
    f.write(ansysInputFile) #write the data into the file
    f.close()

#Define a batch file that we'll call later on. You could even call other programs to run this way
def writeBatchFile(folderLocation):
    f = open( (workFolder+r'\ghAnsys.bat'),'w') #name of batch file we'll use
    batchString = "cd " + folderLocation + "\n" #change working folder of command line
    batchString = batchString + r'"'  +installLocation + r'" -b ' #make sure this matches the location on your computer with an exe file
    batchString = batchString + r'-i "' + folderLocation + r'\ghAnsysInput.txt"'
    batchString = batchString + r' -o "' + folderLocation + r'\ghAnsysOutput.txt"' #this is the Ansys general stats and info file 
    f.write(batchString)
    f.close()


###Execution Code

#provide the location of the solution data files to be used later in GH file
nodeFile = workFolder + r'/nodeOutput.txt'
elemFile = workFolder + r'/elemOutput.txt'

#use a simple switch to write the files and start the analysis if run is true
#you may want to look at modifying the condition if you want Ansys to run
#on every GH state change such as when running optimization methods.
if run:
    writeInputFile(workFolder, ansysFileStrings)
    writeBatchFile(workFolder)
    os.system(workFolder+r'\ghAnsys.bat')