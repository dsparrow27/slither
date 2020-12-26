import glob
import os

from slither import api


class FilesInDirectory(api.PXComputeNode):
    Type = "filesInDirectory"

    def compute(self, context):
        directory = os.path.normpath(context.directory.value())
        if not context.recursive.value():
            context.output.setValue([f for f in glob.glob(os.path.join(directory, "*")) if os.path.isfile(f)])
            return
        outFiles = []
        for root, dirs, files in os.walk(directory):
            outFiles.extend([os.path.join(root, f) for f in files])
        context.output.setValue(outFiles)
