import os

from slither.core import attribute
from slither.core import node


class PathExists(node.BaseNode):
    Type = "PathExists"
    category = "directories"
    documentation = "Checks if file path exists(os.path.exists)"
    file = attribute.AttributeDefinition(isInput=True, type_="file", default="")
    output = attribute.AttributeDefinition(isInput=False, isOutput=True, type_="bool", default=False)

    def execute(self):
        self.output.setValue(os.path.exists(self.file.value()))
