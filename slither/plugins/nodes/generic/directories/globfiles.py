import glob
import os

from slither import api


class Glob(api.PXComputeNode):
    Type = "glob"
    def compute(self, context):
        directory = os.path.normpath(context.directory.value())
        context.output.setValue(glob.glob(os.path.join(directory, context.pattern.value())))
