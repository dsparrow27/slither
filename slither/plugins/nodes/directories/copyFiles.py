import os
import shutil
from slither.core import node
from slither.core import attribute


class CopyFilesToNode(node.BaseNode):
    """Copy a list of files to a directory and returns the new file paths
    """
    source = attribute.InputDefinition(str)
    destinationFolder = attribute.InputDefinition(str)
    result = attribute.OutputDefinition(str)

    def execute(self):
        source = self.source.value()
        destination = self.destinationFolder.value()
        if not os.path.exists(destination) and not os.path.isdir(destination):
            os.mkdir(destination)
        shutil.copy2(source, destination)
        result = os.path.join(destination, os.path.basename(source))
        self.result.setValue(result)
