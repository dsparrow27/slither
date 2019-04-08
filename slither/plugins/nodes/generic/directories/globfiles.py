import glob
import os

from slither.core import attribute
from slither.core import node


class Glob(node.BaseNode):
    Type = "Glob"
    category = "directories"
    documentation = "returns a list of files in a directory"
    directory = attribute.AttributeDefinition(isInput=True, type_="directory", default="", required=True)
    pattern = attribute.AttributeDefinition(isInput=True, type_="str", default="*", required=True)
    output = attribute.AttributeDefinition(isOutput=True, type_="file", array=True, default="")

    def execute(self):
        directory = os.path.normpath(self.directory.value())
        self.output.setValue(glob.glob(os.path.join(directory, self.pattern.value())))
