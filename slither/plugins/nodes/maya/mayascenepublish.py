from pw.libs.shotgun import constants as shotgunConstants
from slither import api


class MayaSceneSaveCompound(api.Compound):
    """Standardized maya scene publish graph

    graph = root.createNode("MayaScenePublish","MayaSceneSave")
    graph.context = utils.currentContext().to_dict()
    graph.template = constants.shot_anim_production_file
    graph.publish = True
    graph.publishDependencies = []
    graph.fields = {"sg_status_list": "cmpt"}

    """
    Type = "mayaSceneSaveCompound"
    context = api.AttributeDefinition(type_=api.types.kDict, isInput=True, array=False,
                                      required=True)
    template = api.AttributeDefinition(type_=api.types.kString, isInput=True, array=False,
                                       required=True)
    publish = api.AttributeDefinition(type_=api.types.kBool, isInput=True, array=False,
                                      required=False,
                                      default=True)
    publishedFileType = api.AttributeDefinition(type_=api.types.kString, isInput=True, array=False,
                                                required=True,
                                                default=shotgunConstants.MA_FILE_TYPE)
    publishDependencies = api.AttributeDefinition(type_=api.types.kFile, isInput=True, array=True,
                                                  required=False,
                                                  default=[])
    fields = api.AttributeDefinition(type_=api.types.kDict, isInput=True, array=True,
                                     required=False,
                                     default=[])

    def mutate(self):
        # pre cache some vars
        ctx = self.context.value()
        # create our nodes
        tankInstance = self.createNode("tank", "CurrentSgtkEngineInstance")
        sceneNode = self.createNode("MayaSceneExporter", "ExportMayaScene")
        incrementPathNode = self.createNode("incrementedPath", "FindLatestPath")

        # do our connections for the path incrementing
        incrementPathNode.tank.connectUpstream(tankInstance.instance)
        incrementPathNode.context.connectUpstream(ctx)
        incrementPathNode.templateName.connectUpstream(self.template.value())

        sceneNode.path.connectUpstream(incrementPathNode.outputPath)

        # create the publish Node if needed and do the connections
        if self.publish.value():
            publish = self.createNode("incrementedPath", "FindLatestPath")
            publish.engine.connectUpstream(tankInstance.instance)
            publish.context.connectUpstream(ctx)
            publish.path.connectUpstream(incrementPathNode.outputPath)
            publish.name.connectUpstream(incrementPathNode.outputName)
            publish.versionNumber.connectUpstream(incrementPathNode.outputVersion)
            publish.dependencyPaths.connectUpstream(self.publishDependencies)
            publish.publishedFileType.connectUpstream(self.publishedFileType)
            publish.sg_fields.connectUpstream(self.fields)
