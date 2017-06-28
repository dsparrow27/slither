Crude implementation of a parallel execution engine in python but without dirty propagation , meant to be used via commandline. Currently we lock up
maya when we use the gui due to maya thinking we want a separate shell which boots mayapy separately, will need to rework this to be
single process when running in the GUI but works fine via commandline, yet to be tested over a farm system.

#general todo
1. unittest
2. single process runner
3. system compound for general use
4. maya processing nodes(I/O)
5. 3dsmax nodes
6. on demand dirty propagation
7. documentation
