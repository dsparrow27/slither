from slither import api


class CurrentMayaScene(api.ComputeNode):
    Type = "currentMayaScene"
    path = api.AttributeDefinition(type_=api.types.kFile, output=True)

    def execute(self, context):
        from maya import OpenMaya as om1
        context.path.setValue(om1.MFileIO.currentFile())
