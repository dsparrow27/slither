from slither import api


class MayaSceneOpen(api.ComputeNode):
    Type = "mayaSceneOpen"
    category = "maya"
    documentation = "Open the supplied maya file"
    sceneFile = api.AttributeDefinition(input=True, type_=api.types.kFile, default="")
    force = api.AttributeDefinition(input=True, type_=api.types.kBool, default="false")

    def execute(self, context):
        from maya import cmds
        path = context.sceneFile.value().replace("\\", "/")
        cmds.file(new=True, force=context.force.value())
        cmds.file(path, open=True, force=True)


class MayaSceneImport(api.ComputeNode):
    Type = "mayaSceneImport"
    category = "maya"
    documentation = "import the supplied maya file"
    sceneFile = api.AttributeDefinition(input=True, type_=api.types.kFile, default="")

    def execute(self, context):
        from maya import cmds
        scene = context.sceneFile.value()

        cmds.file(scene, importFile=True, force=True)


class MayaFBXImport(api.ComputeNode):
    Type = "mayaFBXImport"
    category = "maya"
    documentation = "import the supplied fbx file"
    sceneFile = api.AttributeDefinition(input=True, type_=api.types.kFile, default="")
    constraints = api.AttributeDefinition(input=True, type_=api.types.kBool, default="false")
    skeletonDefinitions = api.AttributeDefinition(input=True, type_=api.types.kBool, default="false")
    lights = api.AttributeDefinition(input=True, type_=api.types.kBool, default="false")
    cameras = api.AttributeDefinition(input=True, type_=api.types.kBool, default="false")

    def execute(self, context):
        from maya import mel
        filepath = context.sceneFile.value().replace("/", "\\")
        mel.eval("FBXImportMode -v add;")
        mel.eval("FBXImportMergeAnimationLayers -v false;")
        mel.eval("FBXImportProtectDrivenKeys -v false;")
        mel.eval("FBXImportConvertDeformingNullsToJoint -v false;")
        mel.eval("FBXImportMergeBackNullPivots -v false;")
        mel.eval("FBXImportSetLockedAttribute -v true;")
        mel.eval("FBXExportConstraints -v {};".format("false" if not context.constraints.value() else "true"))
        mel.eval(
            "FBXExportSkeletonDefinitions -v {};".format("false" if not context.skeletonDefinitions.value() else "true"))
        mel.eval("FBXImportLights -v {};".format(str(context.lights.value()).lower()))
        mel.eval("FBXImportCameras -v {};".format(str(context.cameras.value()).lower()))
        mel.eval("FBXImportHardEdges -v false;")
        mel.eval("FBXImportShapes -v true;")
        mel.eval("FBXImportUnlockNormals -v false;")
        mel.eval('FBXImport -f "{}";'.format(filepath.replace("\\", "/")))  # stupid autodesk and there mel crap


class MayaAbcImport(api.ComputeNode):
    Type = "mayaAlembicImport"
    category = "maya"
    documentation = "import the supplied alembic file"
    filePath = api.AttributeDefinition(input=True, type_=api.types.kFile, default="")

    def execute(self, context):
        from maya import cmds
        filePath = context.filePath.value()
        cmds.AbcImport(filePath, mode="import")
