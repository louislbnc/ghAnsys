# ghAnsys

## Expectations
In it's current state, ghAnsys is simply a minimum example to connect Ansys to Grasshopper. The expectation is for the user to be familiar with both Ansys and Python and use this example as a starting point for their simulation. Hopefully this plumbing solution can save you some time!


### Dependencies
This example file has been tested with Rhino 6.9, Grasshopper 1.0.0007 and Ansys 19.1.

The example contains a simple visualization of the simulation results in the Rhino viewport. This visualization is enabled by [Human 1.1.0](https://www.food4rhino.com/app/human)

## Link Example
The Link example definition contains two main Python scripts:

1. **InputWriter** creates the strings for an Ansys input file that can be dynamically linked to Grasshopper inputs.
1. **Execute** creates an Ansys input file from the strings of InputWriter. It then creates a Batch file which is then run to launch Ansys.

The linkage example is based on [Kent L. Lawrence's work](http://mae.uta.edu/~lawrence/ansys/truss1/truss1.htm).

### Usage
1. Download and open up SimpleLinkExample.gh. The Python scripts are already loaded connected in ghPython components.
2. Change the "installLocation" panel to match the location of your Ansys installation. The file to link is a .exe file which will open up a command prompt running Ansys Mechanical APDL.
3. Change the "workFolder" panel to be a location on your computer on which your Ansys simulation files will reside.
4. Press run!

In order to take this example further, you will need to open up both Python scripts and modify them to suit your simulation needs. Both scripts have ample comments to help you out. 

*Hint:* Consider using the *Network From Lines components* from [Heteroptera](https://www.food4rhino.com/app/heteroptera) in order to easily obtain a Point and Topology set from an unstructured set of lines. 


![Screenshot from Link Example](https://github.com/louislbnc/ghAnsys/blob/master/SimpleLinkScreenshot.PNG "Screenshot from Link Example")

## Future Considerations
Hopefully this simple example can grow into something more meaningful. Namely a simulation on a slid using a mesh as an input as most current solvers integrated with Grasshopper are oriented around structural work. If you have an example file based on ghAnsys, I'd be happy to add it to the repo!

![Example Viewport from a More Complex Simulation](https://github.com/louislbnc/ghAnsys/blob/master/viewportCapture.jpg "Complex Simulation Example")
