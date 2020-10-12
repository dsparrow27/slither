import os
import shutil

from slither import api


class CopyFilesToNode(api.ComputeNode):
    """Copy a list of files to a directory and returns the new file paths
    """
    Type = "copyFilesTo"
    # source = api.AttributeDefinition(input=True, type_=api.types.kFile, isArray=True)
    # destinationFolder = api.AttributeDefinition(input=True, type_=api.types.kDirectory)
    # result = api.AttributeDefinition(output=True, type_=api.types.kFile, isArray=True)

    def execute(self, context):
        source = context.source.value()
        destination = context.destinationFolder.value()
        if not os.path.exists(destination) and not os.path.isdir(destination):
            os.mkdir(destination)
        resultingPaths = []
        count = len(source)
        for index, path in enumerate(source):
            shutil.copy2(path, destination)
            result = os.path.join(destination, os.path.basename(source))
            resultingPaths.append(result)
            context.progress = float(index) / float(count) * 100.0

        context.result.setValue(resultingPaths)
