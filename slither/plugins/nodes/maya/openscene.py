from slither import api


class MayaSceneOpen(api.ComputeNode):
    Type = "mayaSceneOpen"

    def execute(self, context):
        from zoo.libs.maya.utils import files
        files.openFile(context.sceneFile.value(),
                       force=context.force.value())


class MayaSceneImport(api.ComputeNode):
    Type = "mayaSceneImport"

    def execute(self, context):
        from zoo.libs.maya.utils import files
        scene = context.sceneFile.value()
        files.importScene(scene, force=True)


class MayaFBXImport(api.ComputeNode):
    Type = "mayaFBXImport"

    def execute(self, context):
        from zoo.libs.maya.utils import files

        filepath = context.filePath.value().replace("/", "\\")
        files.importFbx(filePath=filepath,
                        cameras=context.cameras.value(),
                        lights=context.lights.value(),
                        skeletonDefinition=context.skeletonDefinitions.value(),
                        constraints=context.constraints.value())


class MayaAbcImport(api.ComputeNode):
    Type = "mayaAlembicImport"

    def execute(self, context):
        from zoo.libs.maya.utils import files
        filePath = context.filePath.value()
        files.importAlembic(filePath)
