Crude implementation of a parallel execution engine in python but without dirty propagation ,
meant to be used via commandline. Currently we lock up maya when we use the gui due to maya thinking we want a 
separate shell which boots mayapy separately, will need to rework this to be single process when running in the 
GUI but works fine via commandline, yet to be tested over a farm system.

:note: This Repo is still WIP

# TODO
1. maya processing nodes(I/O)
2. 3dsmax nodes
3. documentation
4. error handling within nodes
5. up front graph expansion since by default compounds we lazily expand only when we hit a compound not up front.
6. example of creating a graph on the fly.

# Environment variables
These variables store the node and data type library
SLITHER_PLUGIN_PATH

# Supports
Compound nodes eg. nesting nodes within nodes
parallel execution
array attributes
compound attributes
node and datatype library extendability
Graph mutation

# DEPENDENCIES
[Blinker](https://github.com/jek/blinker)
[ffmpeg-python](https://github.com/kkroening/ffmpeg-python)
[ffmpeg](https://www.ffmpeg.org/)

# EXAMPLES

```python

from zoo.core import api
import os
cfg = api.zooFromPath(os.environ["ZOOTOOLS_ROOT"])
cfg.resolver.resolveFromPath(cfg.resolver.environmentPath())

from slither import api

app = api.Application()
graph = app.createGraph(name="mayaTest")
c = graph.createNode("test", type_="sum")
c.inputA.setValue(10)
graph.execute(c, "inProcess") # executes nodes using the inProcess scheduler.
print(c.output.value()) # 10

c.inputB.setValue(50)
graph.execute(c, "parallel") # executes nodes using the parallel scheduler.
print(c.output.value()) # 60
```
