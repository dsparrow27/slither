import os
import shutil
from slither.core import node
from slither.core import attribute


class CopyFilesToNode(node.BaseNode):
    """Copy a list of files to a directory and returns the new file paths
    """
    source = attribute.AttributeDefinition(isInput=True,type_="file", isArray=True)
    destinationFolder = attribute.AttributeDefinition(isInput=True,type_="directory")
    result = attribute.AttributeDefinition(isOutput=True,type_="file", isArray=True)

    def execute(self):
        source = self.source.value()
        destination = self.destinationFolder.value()
        if not os.path.exists(destination) and not os.path.isdir(destination):
            os.mkdir(destination)
        resultingPaths = []
        count = len(source)
        for index, path in enumerate(source):
            shutil.copy2(path, destination)
            result = os.path.join(destination, os.path.basename(source))
            resultingPaths.append(result)
            self.progress = float(index)/float(count) * 100.0

        self.result.setValue(resultingPaths)
