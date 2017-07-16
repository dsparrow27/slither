import os

from slither.core import attribute
from slither.core import node


class FolderInDirectory(node.BaseNode):
    category = "directories"
    documentation = "returns a list of folders in a directory, if recursive is True(default is False) then all subfolders will be returned as well"
    directory = attribute.InputDefinition(type_=str, default="")
    recursive = attribute.InputDefinition(type_=bool, default=False)
    output = attribute.OutputDefinition(type_=str, array=True, default=[])

    def execute(self):
        directory = os.path.normpath(self.directory.value())

        if not self.recursive:
            self.output.setValue([os.path.join(directory, i) for i in os.listdir(directory) if os.path.isdir(i)])
            return
        outFiles = []
        for root, dirs, files in os.walk(directory):
            outFiles.extend([os.path.join(root, d) for d in dirs])
        self.output.setValue(outFiles)