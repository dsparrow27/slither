from slither import api


class MayaSceneOpen(api.PXComputeNode):
    Type = "mayaSceneOpen"

    def compute(self, context):
        from zoo.libs.maya.utils import files
        files.openFile(context.sceneFile.value(),
                       force=context.force.value())


class MayaSceneImport(api.PXComputeNode):
    Type = "mayaSceneImport"

    def compute(self, context):
        from zoo.libs.maya.utils import files
        scene = context.sceneFile.value()
        files.importScene(scene, force=True)


class MayaFBXImport(api.PXComputeNode):
    Type = "mayaFBXImport"

    def compute(self, context):
        from zoo.libs.maya.utils import files

        filepath = context.filePath.value().replace("/", "\\")
        files.importFbx(filePath=filepath,
                        cameras=context.cameras.value(),
                        lights=context.lights.value(),
                        skeletonDefinition=context.skeletonDefinitions.value(),
                        constraints=context.constraints.value())


class MayaAbcImport(api.PXComputeNode):
    Type = "mayaAlembicImport"

    def compute(self, context):
        from zoo.libs.maya.utils import files
        filePath = context.filePath.value()
        files.importAlembic(filePath)
