import os

from slither import api


class FolderInDirectory(api.PXComputeNode):
    Type = "folderInDirectory"

    def compute(self, context):
        directory = os.path.normpath(context.directory.value())

        if not context.recursive.value():
            context.output.setValue([os.path.join(directory, i) for i in os.listdir(directory) if os.path.isdir(i)])
            return
        outFiles = []
        for root, dirs, files in os.walk(directory):
            outFiles.extend([os.path.join(root, d) for d in dirs])
        context.output.setValue(outFiles)
