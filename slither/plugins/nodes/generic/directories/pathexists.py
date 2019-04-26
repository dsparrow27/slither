import os

from slither import api


class PathExists(api.ComputeNode):
    Type = "PathExists"
    category = "directories"
    documentation = "Checks if file path exists(os.path.exists)"
    file = api.AttributeDefinition(input=True, type_=api.types.kFile, default="")
    output = api.AttributeDefinition(input=False, output=True, type_=api.types.kBool, default=False)

    def execute(self, context):
        self.output.setValue(os.path.exists(self.file.value()))
