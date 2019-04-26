from slither import api


class CurrentMayaScene(api.ComputeNode):
    Type = "currentMayaScene"
    path = api.AttributeDefinition(type_=api.types.kFile, input=True)

    def execute(self, context):
        from maya import OpenMaya as om1
        self.path.setValue(om1.MFileIO.currentFile())
