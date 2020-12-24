from zoo.core import api

cfg = api.zooFromPath(os.environ["ZOOTOOLS_ROOT"])
cfg.resolver.resolveFromPath(cfg.resolver.environmentPath())

# import os, sys
# p = os.environ["SLITHER_PLUGIN_PATH"] =r"F:\code\python\personal\slither\slither\plugins"
sys.path.append(r"F:\code\python\personal\slither")
from slither import api

app = api.Application()
graph = app.createGraph(name="mayaTest")

createCube = graph.createNode(name="createCube", type_="python")
createCube.script = r"from maya import cmds; cube = cmds.polyCube();print(cube)"

graph.execute(graph.root, app.STANDARDEXECUTOR)
