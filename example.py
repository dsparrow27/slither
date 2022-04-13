from zoo.core import api
import os
cfg = api.zooFromPath(os.environ["ZOOTOOLS_PRO_ROOT"])
cfg.resolver.resolveFromPath(cfg.resolver.environmentPath())

from slither import api

app = api.Application()
graph = app.createGraph(name="mayaTest")
c = graph.createNode("test", type_="compound")
graph.createNode("test", type_="python", parent=c)
print(graph.root.children)
print(c.children)
