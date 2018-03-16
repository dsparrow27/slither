"""type constants module
"""
from . import typeregistry
from . import nodeRegistry

ourdict = globals()

for _v, _typ in typeregistry.DataTypeRegistry().dataTypes.items():
    ourdict["k"+str(_v)] = _typ

for _v, _typ in nodeRegistry.NodeRegistry().nodes.items():
    ourdict["k"+str(_v)] = _typ