import glob
import os

from slither import api


class Glob(api.ComputeNode):
    Type = "Glob"
    category = "directories"
    documentation = "returns a list of files in a directory"
    directory = api.AttributeDefinition(input=True, type_=api.types.kDirectory, default="", required=True)
    pattern = api.AttributeDefinition(input=True, type_=api.types.kString, default="*", required=True)
    output = api.AttributeDefinition(output=True, type_=api.types.kFile, array=True, default="")

    def execute(self, context):
        directory = os.path.normpath(context.directory.value())
        context.output.setValue(glob.glob(os.path.join(directory, context.pattern.value())))
