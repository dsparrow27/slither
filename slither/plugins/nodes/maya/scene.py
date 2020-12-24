from slither import api


class CurrentMayaScene(api.PXComputeNode):
    Type = "currentMayaScene"

    def compute(self, context):
        from maya import OpenMaya as om1
        context.path.setValue(om1.MFileIO.currentFile())
