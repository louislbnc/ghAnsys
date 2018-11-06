"""This component takes various inputs and cobbles them together into a string that is a 
usable Ansys input. 

This python component is intended to be modified by the users to suit their own simulation
needs. For this reason, there's a reasonable expection of understanding of Python
and Ansys from the end user. Hopefully this component can be expanded on in the future
and provide simpler methods for the user...

Right now a lot of the simulation parameters are hard coded in this file. However, this
is a very practical way of putting together the Ansys input file. I recomend using
the Ansys Mechanical with the GUI interface to setup your simulation. Then you can 
look at the commands that were used in the log. You can use that log file as a basis 
for your integration with your Grasshopper definition.

    Inputs:
        nodes: list of points that will be used to describe the 
        
        topo: provde the pair of points to be used as the lines that form each element here
        format is list item number, list item number or 0,1 to connect point 0 to 1.
        
        force: right now force is hard codded to be a force applied on one of the nodes is y direction.
        

    Outputs:
        
        ansysFileStrings: this is the output in the form of the raw text for an Ansys input
"""
        
__author__ = "Louis Leblanc"
__version__ = "2018.11.05"

#use 'text' as a running variable to hold our whole file
#start by adding the Ansys header
text='''
/FILNAM,truss
/title, Simple Truss
/prep7

'''

#print nodes. These denote the ends of the elements
for point in range(len(nodes)):
    #note we're starting with node 1 rather than node 0 as we had it in GH
    text = text + ("n, "+ str(point+1)+ ", " +  nodes[point] +"\n")

#add functionalities here later on but we're defining the properties of the elements
text = text + '''
et, 1, link180             ! Element type; no.1 is link180
sectype, 1, link           ! Type of cross section is link 
secdata, 697e-6            ! Cross sectional area = 0.5 sq in
mp, ex, 1, 200e3           !  material property #1; Young's modulus: 200 GPa
mp, prxy, 1, 0.3           ! & poisson's ratio for material no.1

'''

#print elements
for currentLine in range(len(topo)):
    #seperate the two values we've given into a Python list
    elem = topo[currentLine].split(",")
    #make the strings into ints and add 1 to them as the points in Ansys
    #start at 1 and not 0 like we had in GH
    elem= [int(i)+1 for i in elem]
    #join the two numbers back into a str
    elem = ",".join([str(x) for x in elem])
    #finally make the line of text
    text = text + ("en, "+ str(currentLine+1)+ ", " + elem   +"\n")

#print boundary conditions - again this is hard coded for now
#using a similar strategy as was used for writing the elements
#and nodes, these could be linked to 
text = text+ '''
d, 3, ux, 0.             ! Displacement at node 3 in x-dir is zero
d, 3, uy, 0.             ! Displacement at node 3 in y-dir is zero
d, 2, ux, 0.
d, 2, uy, 0.
d, 4, ux, 0.
d, 4, uy, 0.

'''

#print force value
text = text + ("f, 1, fy, " + str(force))

#print command to run the simulation and include all the post processing code
text = text + '''
finish
/solu                    ! Select static load solution
antype, static
solve
finish
save
/post1                   ! Use 'ssum' to compute sums interactively
!alls
'''

#we now print the post processing which will give us the nodal displacement
#you could modify this part to include other data you may want
#horay for Fortran, not.
text = text + '''
!make a CSV for nodal data
*CFOPEN,nodeOutput,txt

*GET,num_nodes_,NODE,0,COUNT !Get the number of nodes
*GET,node_,NODE,0,NUM,MIN !Get label of the first node

*DO,i,1,num_nodes_,1
  ! Define some parameters - we're getting the displacement
  *GET,nx_,NODE,node_,U,X
  *GET,ny_,NODE,node_,U,Y
  *GET,nz_,NODE,node_,U,Z
  !NSOL can be used for other values
  
  ! Write line
  *VWRITE,nx_,ny_,nz_
  (E10.3,',',E10.3,',',E10.3)
  
  ! select the next node
  *GET,node_,NODE,node_,NXTH
  
*ENDDO
*CFCLOSE
'''

#We now print the command to get the results for the elements. More
#queries could be done at this point. I'm also including a portion that's
#commented out to get a PRESOL - this could be useful for debuging as it
#gives a lot more context than ESOL which is element by element.
#

text = text+ '''

!Create an ETABLE with the axial stress
ETABLE,myTable,LS, 1

!Uncomment this to print out the etable
!/output,etablePrint,out
!PRETAB,myTable
!/out

!PRINTS THE STRESS VALUES LINE BY LINE TO A FILE
*CFOPEN,elemOutput,txt
*GET,num_elems_,ELEM,0,COUNT !Get the number of elems
*GET,elem_,ELEM,0,NUM,MIN !Get label of the first elems

*DO,i,1,num_elems_,1
  ! Define some parameters
  *GET,seqv,ETAB,1,ELEM,elem_

  ! Write line
  *VWRITE,seqv
  (E10.3)
  
  ! select the next elem
  *GET,elem_,ELEM,elem_,NXTH

*ENDDO
*CFCLOSE

!Uncomment this to get the regular print by elements
!/output,print_output,txt     ! redirect output to a file called "print_output.txt"
!PRESOL,S, PRNT
'''

ansysFileStrings= text