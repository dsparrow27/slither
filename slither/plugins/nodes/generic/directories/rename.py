import math
import os

from slither import api


class Rename(api.ComputeNode):
    Type = "Rename"
    category = "directories"
    documentation = "Rename"
    file = api.AttributeDefinition(isInput=True, type_=api.types.kFile, default="")
    name = api.AttributeDefinition(isInput=True, type_=api.types.kString, default="")

    def execute(self, context):
        self.output.setValue(math.pi)
        os.rename(self.file.value(), self.name.value())
