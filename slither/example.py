from zoo.core import api
import os


if __name__ == "__main__":
    cfg = api.zooFromPath(os.environ["ZOOTOOLS_ROOT"])
    cfg.resolver.resolveFromPath(cfg.resolver.environmentPath())
    from slither import api    
    g = api.Graph()
    g.initialize()
    n = g.createNode("test", "FilesInDirectory")
    n.directory.setValue(r"C:/Users/dave/Desktop")
    n.recursive.setValue(False)
    n.output.setValue([r"C:\Users\dave\Desktop\bo"])
    ctx = api.Context.fromNode(n)
    ctx.output.setValue(["test"])
    g.execute(g.root,g.STANDARDEXECUTOR)
    print(n.output.value())