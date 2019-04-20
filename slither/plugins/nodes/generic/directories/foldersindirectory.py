import os

from slither import api


class FolderInDirectory(api.ComputeNode):
    Type = "FolderInDirectory"
    category = "directories"
    documentation = "returns a list of folders in a directory, if recursive is True(default is False) then all " \
                    "subfolders will be returned as well"
    directory = api.AttributeDefinition(isInput=True, type_=api.types.kDirectory, default="")
    recursive = api.AttributeDefinition(isInput=True, type_=api.types.kBool, default=False)
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kDirectory, array=True, default=[])

    def execute(self):
        directory = os.path.normpath(self.directory.value())

        if not self.recursive.value():
            self.output.setValue([os.path.join(directory, i) for i in os.listdir(directory) if os.path.isdir(i)])
            return
        outFiles = []
        for root, dirs, files in os.walk(directory):
            outFiles.extend([os.path.join(root, d) for d in dirs])
        self.output.setValue(outFiles)
