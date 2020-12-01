from slither import api


class CurrentMayaScene(api.ComputeNode):
    Type = "currentMayaScene"

    def execute(self, context):
        from maya import OpenMaya as om1
        context.path.setValue(om1.MFileIO.currentFile())
