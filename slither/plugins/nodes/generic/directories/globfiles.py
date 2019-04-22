import glob
import os

from slither import api


class Glob(api.ComputeNode):
    Type = "Glob"
    category = "directories"
    documentation = "returns a list of files in a directory"
    directory = api.AttributeDefinition(isInput=True, type_=api.types.kDirectory, default="", required=True)
    pattern = api.AttributeDefinition(isInput=True, type_=api.types.kString, default="*", required=True)
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kFile, array=True, default="")

    def execute(self, context):
        directory = os.path.normpath(self.directory.value())
        self.output.setValue(glob.glob(os.path.join(directory, self.pattern.value())))
