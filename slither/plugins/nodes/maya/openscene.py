from slither import api


class MayaSceneOpen(api.BaseNode):
    Type = "mayaSceneOpen"
    category = "maya"
    documentation = "Open the supplied maya file"
    sceneFile = api.AttributeDefinition(isInput=True, type_=api.types.kFile, default="")
    force = api.AttributeDefinition(isInput=True, type_=api.types.kFile, default="")

    def execute(self):
        from maya import cmds
        path = self.sceneFile.value().replace("\\", "/")
        cmds.file(new=True, force=self.force.value())
        cmds.file(path, open=True, force=True)


class MayaSceneImport(api.BaseNode):
    Type = "mayaSceneImport"
    category = "maya"
    documentation = "import the supplied maya file"
    sceneFile = api.AttributeDefinition(isInput=True, type_=api.types.kFile, default="")

    def execute(self):
        from maya import cmds
        scene = self.sceneFile.value()

        cmds.file(scene, importFile=True, force=True)


class MayaFBXImport(api.BaseNode):
    Type = "mayaFBXImport"
    category = "maya"
    documentation = "import the supplied fbx file"
    sceneFile = api.AttributeDefinition(isInput=True, type_=api.types.kFile, default="")
    constraints = api.AttributeDefinition(isInput=True, type_=api.types.kBool, default="false")
    skeletonDefinitions = api.AttributeDefinition(isInput=True, type_=api.types.kBool, default="false")
    lights = api.AttributeDefinition(isInput=True, type_=api.types.kBool, default="false")
    cameras = api.AttributeDefinition(isInput=True, type_=api.types.kBool, default="false")

    def execute(self):
        from maya import mel
        filepath = self.sceneFile.value().replace("/", "\\")
        mel.eval("FBXImportMode -v add;")
        mel.eval("FBXImportMergeAnimationLayers -v false;")
        mel.eval("FBXImportProtectDrivenKeys -v false;")
        mel.eval("FBXImportConvertDeformingNullsToJoint -v false;")
        mel.eval("FBXImportMergeBackNullPivots -v false;")
        mel.eval("FBXImportSetLockedAttribute -v true;")
        mel.eval("FBXExportConstraints -v {};".format("false" if not self.constraints.value() else "true"))
        mel.eval(
            "FBXExportSkeletonDefinitions -v {};".format("false" if not self.skeletonDefinitions.value() else "true"))
        mel.eval("FBXImportLights -v {};".format(str(self.lights.value()).lower()))
        mel.eval("FBXImportCameras -v {};".format(str(self.cameras.value()).lower()))
        mel.eval("FBXImportHardEdges -v false;")
        mel.eval("FBXImportShapes -v true;")
        mel.eval("FBXImportUnlockNormals -v false;")
        mel.eval('FBXImport -f "{}";'.format(filepath.replace("\\", "/")))  # stupid autodesk and there mel crap


class MayaAbcImport(api.BaseNode):
    Type = "mayaAlembicImport"
    category = "maya"
    documentation = "import the supplied alembic file"
    filePath = api.AttributeDefinition(isInput=True, type_=api.types.kFile, default="")

    def execute(self):
        from maya import cmds
        filePath = self.filePath.value()
        cmds.AbcImport(filePath, mode="import")
