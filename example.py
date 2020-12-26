from zoo.core import api
import os
cfg = api.zooFromPath(os.environ["ZOOTOOLS_ROOT"])
cfg.resolver.resolveFromPath(cfg.resolver.environmentPath())


# import os, sys
# p = os.environ["SLITHER_PLUGIN_PATH"] =r"F:\code\python\personal\slither\slither\plugins"
#sys.path.append(r"F:\code\python\personal\slither")
from slither import api
from slither.core import visualize

app = api.Application()
graph = app.createGraph(name="mayaTest")
graph.loadFromFile(r"D:\dave\code\python\tools\personal\slither\tests\data\testGraph.slgraph")
# visualize.buildGraph(graph.root, r"D:\dave\downloads\graphviz-2.44.1-win32\Graphviz\test.png")
# createCube = graph.createNode(name="createCube", type_="python")
# createCube.script = r"from maya import cmds; cube = cmds.polyCube();print(cube)"
#
# graph.execute(graph.root, app.STANDARDEXECUTOR)
