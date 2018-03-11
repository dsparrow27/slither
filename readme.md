Crude implementation of a parallel execution engine in python but without dirty propagation , meant to be used via commandline. Currently we lock up maya when we use the gui due to maya thinking we want a separate shell which boots mayapy separately, will need to rework this to be single process when running in the GUI but works fine via commandline, yet to be tested over a farm system.

:note:: This Repo is still WIP

# TODO
1. unittest
2. single process runner
3. system compound for general use
4. maya processing nodes(I/O)
5. 3dsmax nodes
6. on demand dirty propagation
7. documentation
8. error handling within nodes
9. Skip attribute and node initialization if a node fails to initialize
10. up front graph expansion since by default compounds we lazily expand only when we hit a compound not up front.
11. example of creating a graph on the fly.
12. deserialize a graph from json

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

# DEPENDENCIES
[Blinker](https://github.com/jek/blinker)

# EXAMPLES

```python

import os
import sys
from slither import api
from slither.core import executor

app = api.initialize()
root = app.root

testSum = app.createNode("testNode", type_="Sum")

executor.StandardExecutor().execute(root)
# pprint the graph
pprint.pprint(root.serialize())
# get the final result for the graph
print root.execution.value()
```
