import os

from slither import api
from zoo.libs.maya.utils import files

class ExportAlembicCamera(api.ComputeNode):
    Type = "exportAlembicCamera"
    category = "maya"
    documentation = ""
    path = api.AttributeDefinition(input=True, type_=api.types.kFile, array=False, default="")
    camera = api.AttributeDefinition(input=True, type_=api.types.kMObjectHandle, array=False, default=None)
    output = api.AttributeDefinition(output=True, type_=api.types.kBool, array=False, default=False)
    startFrame = api.AttributeDefinition(input=True, type_=api.types.kInt, array=False, default=0)
    endFrame = api.AttributeDefinition(input=True, type_=api.types.kInt, array=False, default=0)
    subFrames = api.AttributeDefinition(input=True, type_=api.types.kFloat, array=False, default=0)
    cameraName = api.AttributeDefinition(input=True, type_=api.types.kString, array=False, default="NO_NAME",
                                         required=True
                                         )
    force = api.AttributeDefinition(input=True, type_=api.types.kBool, array=False, default=False,
                                    required=False)
    padding = api.AttributeDefinition(input=True, type_=api.types.kInt, array=False, default=0,
                                      required=False)

    def validate(self):
        camera = self.camera.value()
        if not camera.isValid() or not camera.isAlive():
            raise ValueError
        outputPath = self.path.value()
        if os.path.exists(outputPath) and not self.force.value():
            raise OSError("Path already exists: {}".format(outputPath))

    def execute(self, context):
        from maya.api import OpenMaya as om2


        self.validate()
        camera = self.camera.value()
        outputPath = self.path.value()

        cameraPath = om2.MDagPath.getAPathTo(camera.object())

        startFrame = self.startFrame.value() - self.padding.value()
        endFrame = self.endFrame.value() + self.padding.value()
        files.exportAbc(outputPath,
                        cameraPath.fullPathName(),
                        "{:d} {:d}".format(startFrame, endFrame),
                        subframeValue=self.subFrames.value())
        self.output.setValue(True)


class ExportFBXCamera(api.ComputeNode):
    Type = "exportFBXCamera"
    category = "maya"
    documentation = ""
    path = api.AttributeDefinition(input=True, type_=api.types.kFile, array=False, default="")
    camera = api.AttributeDefinition(input=True, type_=api.types.kMObjectHandle, array=False, default=None)
    output = api.AttributeDefinition(output=True, type_=api.types.kBool, array=False, default=False)
    startFrame = api.AttributeDefinition(input=True, type_=api.types.kInt, array=False, default=0)
    endFrame = api.AttributeDefinition(input=True, type_=api.types.kInt, array=False, default=0)
    subFrames = api.AttributeDefinition(input=True, type_=api.types.kFloat, array=False, default=0)
    cameraName = api.AttributeDefinition(input=True, type_=api.types.kString, array=False, default="NO_NAME",
                                         required=True
                                         )
    force = api.AttributeDefinition(input=True, type_=api.types.kBool, array=False, default=False,
                                    required=False)
    padding = api.AttributeDefinition(input=True, type_=api.types.kInt, array=False, default=0,
                                      required=False)

    def validate(self):
        camera = self.camera.value()
        if not camera.isValid() or not camera.isAlive():
            raise ValueError
        outputPath = self.path.value()
        if os.path.exists(outputPath) and not self.force.value():
            raise OSError("Path already exists: {}".format(outputPath))

    def execute(self, context):
        from maya.api import OpenMaya as om2
        from pw.libs.maya.utils import files

        self.validate()
        camera = self.camera.value()
        outputPath = self.path.value()

        cameraPath = om2.MDagPath.getAPathTo(camera.object())

        startFrame = self.startFrame.value() - self.padding.value()
        endFrame = self.endFrame.value() + self.padding.value()
        files.exportFbx(outputPath,
                        cameraPath.fullPathName(),
                        skeletonDefinition=False,
                        constraints=False,
                        shapes=False,
                        lights=False,
                        cameras=True,
                        animation=True,
                        startFrame=startFrame,
                        endFrame=endFrame,
                        step=self.subFrames.value())
        self.output.setValue(True)
