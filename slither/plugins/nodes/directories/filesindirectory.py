import os

from slither.core import attribute
from slither.core import node


class FilesInDirectory(node.BaseNode):
    category = "directories"
    documentation = "returns a list of files in a directory"
    directory = attribute.AttributeDefinition(isInput=True,type_=str, default="")
    recursive = attribute.AttributeDefinition(isInput=True,type_=bool, default=False)
    output = attribute.AttributeDefinition(isOutput=True,type_=str, array=True, default=[])

    def execute(self):
        directory = os.path.normpath(self.directory.value())

        if not self.recursive:
            self.output.setValue([os.path.join(directory, i) for i in os.listdir(directory) if os.path.isfile(i)])
            return
        outFiles = []
        for root, dirs, files in os.walk(directory):
            outFiles.extend([os.path.join(root, f) for f in files])
        self.output.setValue(outFiles)
