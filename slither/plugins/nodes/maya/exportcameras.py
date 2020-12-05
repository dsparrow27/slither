import os

from slither import api


class ExportAlembicCamera(api.ComputeNode):
    Type = "exportAlembicCamera"

    def validate(self, context):
        camera = context.camera.value()
        if not camera.isValid() or not camera.isAlive():
            raise ValueError
        outputPath = context.path.value()
        if os.path.exists(outputPath) and not context.force.value():
            raise OSError("Path already exists: {}".format(outputPath))

    def execute(self, context):
        from zoo.libs.maya.utils import files
        from maya import cmds

        self.validate(context)
        camera = context.camera.value()
        outputPath = context.path.value()
        if not cmds.objExists(camera):
            raise ValueError("Missing Camera in the scene: {}".format(camera))

        startFrame = context.startFrame.value() - context.padding.value()
        endFrame = context.endFrame.value() + context.padding.value()
        files.exportAbc(outputPath,
                        camera,
                        "{:d} {:d}".format(startFrame, endFrame),
                        subframeValue=context.subFrames.value())
        context.output.setValue(True)


class ExportFBXCamera(api.ComputeNode):
    Type = "exportFBXCamera"

    def validate(self, context):
        camera = context.camera.value()
        if not camera.isValid() or not camera.isAlive():
            raise ValueError
        outputPath = context.path.value()
        if os.path.exists(outputPath) and not context.force.value():
            raise OSError("Path already exists: {}".format(outputPath))

    def execute(self, context):
        from zoo.libs.maya.utils import files

        self.validate(context)
        camera = context.camera.value()
        outputPath = context.path.value()
        startFrame = context.startFrame.value() - context.padding.value()
        endFrame = context.endFrame.value() + context.padding.value()
        files.exportFbx(outputPath,
                        camera,
                        skeletonDefinition=False,
                        constraints=False,
                        shapes=False,
                        lights=False,
                        cameras=True,
                        animation=True,
                        startFrame=startFrame,
                        endFrame=endFrame,
                        step=context.subFrames.value())
        context.output.setValue(True)
