import glob
import os

from slither import api


class FilesInDirectory(api.ComputeNode):
    Type = "FilesInDirectory"
    category = "directories"
    documentation = "returns a list of files in a directory"
    directory = api.AttributeDefinition(isInput=True, type_=api.types.kDirectory, default="")
    recursive = api.AttributeDefinition(isInput=True, type_=api.types.kBool, default=False)
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kFile, array=True, default=[])

    def execute(self, context):
        directory = os.path.normpath(self.directory.value())

        if not self.recursive.value():
            self.output.setValue([f for f in glob.glob(os.path.join(directory, "*")) if os.path.isfile(f)])
            return
        outFiles = []
        for root, dirs, files in os.walk(directory):
            outFiles.extend([os.path.join(root, f) for f in files])
        self.output.setValue(outFiles)
