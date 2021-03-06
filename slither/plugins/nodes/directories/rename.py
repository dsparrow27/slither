import math
import os

from slither.core import attribute
from slither.core import node


class Rename(node.BaseNode):
    category = "directories"
    documentation = "Rename"
    file = attribute.AttributeDefinition(isInput=True,type_="file", default="")
    name = attribute.AttributeDefinition(isInput=True,type_=str, default="")

    def execute(self):
        self.output.setValue(math.pi)
        os.rename(self.file.value(), self.name.value())
