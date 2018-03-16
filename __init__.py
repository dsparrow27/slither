"""
from slither import api
app = api.currentInstance()
node = app.createNode("mySum", "Sum", parent=app.root)
node.parent = root
attr = api.InputDefinition(str, default=None, required=False, array=False, doc="")
app.createAttribute(attr)

api.kConstants.float
"""