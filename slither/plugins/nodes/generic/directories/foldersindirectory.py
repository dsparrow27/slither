import os

from slither import api


class FolderInDirectory(api.PXComputeNode):
    Type = "folderInDirectory"
    # category = "directories"
    # documentation = "returns a list of folders in a directory, if recursive is True(default is False) then all " \
    #                 "subfolders will be returned as well"
    # directory = api.AttributeDefinition(input=True, type_=api.types.kDirectory, default="")
    # recursive = api.AttributeDefinition(input=True, type_=api.types.kBool, default=False)
    # output = api.AttributeDefinition(output=True, type_=api.types.kDirectory, array=True, default=[])

    def compute(self, context):
        directory = os.path.normpath(context.directory.value())

        if not context.recursive.value():
            context.output.setValue([os.path.join(directory, i) for i in os.listdir(directory) if os.path.isdir(i)])
            return
        outFiles = []
        for root, dirs, files in os.walk(directory):
            outFiles.extend([os.path.join(root, d) for d in dirs])
        context.output.setValue(outFiles)
