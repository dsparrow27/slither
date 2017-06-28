Crude implementation of a parallel execution engine in python but without dirty propagation , meant to be used via commandline. Currently we lock up maya when we use the gui due to maya thinking we want a separate shell which boots mayapy separately, will need to rework this to be single process when running in the GUI but works fine via commandline, yet to be tested over a farm system.



# TODO
1. unittest
2. single process runner
3. system compound for general use
4. maya processing nodes(I/O)
5. 3dsmax nodes
6. on demand dirty propagation
7. documentation
8. error handling within nodes
9. local graph variables similar to environment variable but at the graph level
10 high level application configuration
11. Skip attribute and node initialization if a node fails to initialize
12. up front graph expansion since by default compounds we lazily expand only when we hit a compound not up front.
13. example of creating a graph on the fly.
14. deserialize a graph from json

# Environment variables
These variables store the node and data type library, you can add your own directory paths once slither is initialized
SLITHER_NODE_LIB
SLITHER_TYPE_LIB

# Supports
Compound nodes eg. nesting nodes within nodes
parallel execution
array attributes
compound attributes
node and datatype library extendability
Graph mutation


# EXAMPLES

```python

import os
import sys
from slither.core import nodeRegistry
from slither.core import typeregistry
import graphtest
from slither import startup
root = graphtest.TestCompound("root")
executor.StandardExecutor().execute(root)
# pprint the graph
pprint.pprint(root.serialize())
# get the final result for the graph
print root.execution.value()
```