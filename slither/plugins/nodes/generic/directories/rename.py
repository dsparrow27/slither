import math
import os

from slither import api


class Rename(api.ComputeNode):
    Type = "Rename"
    category = "directories"
    documentation = "Rename"
    file = api.AttributeDefinition(input=True, type_=api.types.kFile, default="")
    name = api.AttributeDefinition(input=True, type_=api.types.kString, default="")

    def execute(self, context):
        context.output.setValue(math.pi)
        os.rename(context.file.value(), context.name.value())
