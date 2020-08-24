import os

from slither import api


class ExportMayaScene(api.ComputeNode):
    Type = "exportMayaScene"
    category = "maya"
    documentation = ""
    path = api.AttributeDefinition(input=True, type_=api.types.kFile, array=False, default="")
    output = api.AttributeDefinition(output=True, type_=api.types.kBool, array=False, default=False)
    force = api.AttributeDefinition(input=True, type_=api.types.kBool, array=False, default=False,
                                    required=False)

    def execute(self, context):

        from zoo.libs.maya.utils import files
        outputPath = context.path.value()
        if not outputPath:
            raise ValueError("No path specified")
        if os.path.exists(outputPath) and not context.force.value():
            raise OSError("Path already exists!: {}".format(outputPath))
        try:
            files.saveScene(outputPath)
            context.output.setValue(True)
        except Exception:
            context.output.setValue(False)
