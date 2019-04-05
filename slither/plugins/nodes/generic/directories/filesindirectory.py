import glob
import os

from slither.core import attribute
from slither.core import node


class FilesInDirectory(node.BaseNode):
    Type = "FilesInDirectory"
    category = "directories"
    documentation = "returns a list of files in a directory"
    directory = attribute.AttributeDefinition(isInput=True, type_="directory", default="")
    recursive = attribute.AttributeDefinition(isInput=True, type="bool", default=False)
    output = attribute.AttributeDefinition(isOutput=True, type_="file", array=True, default=[])

    def execute(self):
        directory = os.path.normpath(self.directory.value())

        if not self.recursive.value():
            self.output.setValue([f for f in glob.glob(os.path.join(directory, "*")) if os.path.isfile(f)])
            return
        outFiles = []
        for root, dirs, files in os.walk(directory):
            outFiles.extend([os.path.join(root, f) for f in files])
        self.output.setValue(outFiles)
