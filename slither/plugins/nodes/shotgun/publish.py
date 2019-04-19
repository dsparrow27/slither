from slither import api


class PublishCompound(api.Compound):
    Type = "PublishCompound"
    category = "Shotgun"
    path = api.AttributeDefinition(type_=api.types.kFile, isInput=True)

    description = api.AttributeDefinition(type_=api.types.kString, isInput=True)
    templateName = api.AttributeDefinition(type_=api.types.kString, isInput=True)
    fields = api.AttributeDefinition(type_=api.types.kDict, isInput=True)
    dryRun = api.AttributeDefinition(type_=api.types.kBool, isInput=True)
    thumbnail = api.AttributeDefinition(type_=api.types.kFile, isInput=True)
    publishType = api.AttributeDefinition(type_=api.types.kString, isInput=True)
    dependencies = api.AttributeDefinition(type_=api.types.kList, isInput=True)

    def mutate(self):
        if self.child("tank"):
            return

        currentTankNode = self.createNode("tank", "sgtkEngineInstance")
        copyNode = self.createNode("copyFiles", "copyFilesTo")
        latestPathNode = self.createNode("latestPath", "FindLatestPath")
        publishNode = self.createNode("shotgunPublish", "shotgunTankPublish")

        copyNode.source.connectUpstream(self.path)
        copyNode.destinationFolder.connectUpstream(latestPathNode.outputPath)
        latestPathNode.tank.connectUpstream(currentTankNode.instance)
        latestPathNode.context.connectUpstream(currentTankNode.context)
        latestPathNode.templateName.connectUpstream(self.templateName)
        latestPathNode.fields.connectUpstream(self.fields)

        publishNode.engine.connectUpstream(currentTankNode.instance)
        publishNode.context.connectUpstream(currentTankNode.context)
        publishNode.comment.connectUpstream(self.description)
        publishNode.path.connectUpstream(latestPathNode.outputPath)
        publishNode.name.connectUpstream(latestPathNode.outputName)
        publishNode.versionNumber.connectUpstream(latestPathNode.outputVersion)
        publishNode.thumbnailPath.connectUpstream(self.thumbnail)
        publishNode.publishedFileType.connectUpstream(self.publishType)
        publishNode.dependencyPaths.connectUpstream(self.dependencies)
        publishNode.sg_fields.connectUpstream(self.fields)
        publishNode.dry_run.connectUpstream(self.dryRun)
