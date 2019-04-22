import os

from slither import api


class ExportMayaScene(api.ComputeNode):
    Type = "exportMayaScene"
    category = "maya"
    documentation = ""
    path = api.AttributeDefinition(isInput=True, type_=api.types.kFile, array=False, default="")
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kBool, array=False, default=False)
    force = api.AttributeDefinition(isInput=True, type_=api.types.kBool, array=False, default=False,
                                    required=False)

    def execute(self, context):

        from pw.libs.maya.utils import files
        outputPath = self.path.value()
        if not outputPath:
            raise ValueError("No path specified")
        if os.path.exists(outputPath) and not self.force.value():
            raise OSError("Path already exists!: {}".format(outputPath))
        try:
            files.saveScene(outputPath)
            self.output.setValue(True)
        except Exception:
            self.output.setValue(False)
