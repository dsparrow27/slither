import logging
import os
import pprint
import sys

from slither import api

logger = logging.getLogger(__name__)


class DestroyTankEngine(api.ComputeNode):
    Type = "DestroyTankEngine"
    category = "shotgun"
    documentation = "Destroys the shotgun toolkit engine by calling destroy_engine on the instance"
    engine = api.AttributeDefinition(output=True, type_=api.types.ksgtkEngine, array=False, default=None)

    def execute(self, context):
        if self.engine is not None:
            self.engine.destroy_engine()


class InitTankEngine(api.ComputeNode):
    Type = "InitTankEngine"
    category = "shotgun"
    documentation = "Initializes a shotgun tank instance using the supplied environment"

    modulePath = api.AttributeDefinition(input=True, type_=api.types.kString, array=False, default="")
    apiScript = api.AttributeDefinition(input=True, type_=api.types.kString, array=False, default="")
    context = api.AttributeDefinition(input=True, type_=api.types.kDict, array=False, default=dict())
    apiKey = api.AttributeDefinition(input=True, type_=api.types.kString, default="")
    host = api.AttributeDefinition(input=True, type_=api.types.kString, default="")
    configUri = api.AttributeDefinition(input=True, type_=api.types.kString, default="")
    plugins = api.AttributeDefinition(input=True, type_=api.types.kString, default="")
    engine_name = api.AttributeDefinition(input=True, type_=api.types.kString, default="")
    engine = api.AttributeDefinition(output=True, type_=api.types.ksgtkEngine, array=False, default=None)

    def execute(self, context):
        context = self.context.value()
        if not context or not any(i in context.keys() for i in ("SHOTGUN_ENTITY_ID", "SHOTGUN_ENTITY_TYPE")):
            raise ValueError("Incorrect argument context values, must have only:{}, supplied: {}".format(
                str(("SHOTGUN_ENTITY_ID", "SHOTGUN_ENTITY_TYPE")),
                str(context)))
        os.environ.update(context)
        TK_CORE_PATH = self.modulePath.value()
        if TK_CORE_PATH and TK_CORE_PATH not in sys.path:
            sys.path.append(TK_CORE_PATH)

        import sgtk
        engine = sgtk.platform.current_engine()
        if engine is not None:
            self.engine = engine
            return
        # Authenticate using a pre-defined script user.
        sa = sgtk.authentication.ShotgunAuthenticator()
        user = sa.create_script_user(
            api_script=self.apiScript.value(),
            api_key=self.apiKey.value(),
            host=self.host.value()
        )
        mgr = sgtk.bootstrap.ToolkitManager(sg_user=user)

        mgr.base_configuration = self.configUri.value()

        mgr.do_shotgun_config_lookup = False

        mgr.plugin_id = self.plugins.value()
        sg_entity = mgr.get_entity_from_environment()

        engine = mgr.bootstrap_engine(self.engine_name.value(), entity=sg_entity)
        self.engine = engine


class ShotgunTankPublish(api.ComputeNode):
    Type = "ShotgunTankPublish"
    category = "shotgun"
    documentation = "Publishes the file to shotgun using tank.util.register_publish"
    engine = api.AttributeDefinition(output=True, type_=api.types.ksgtkEngine, array=False, default=None)
    context = api.AttributeDefinition(input=True, type_=api.types.kDict, default=dict())
    comment = api.AttributeDefinition(input=True, type_=api.types.kString, default="")
    path = api.AttributeDefinition(input=True, type_=api.types.kString, default="")
    name = api.AttributeDefinition(input=True, type_=api.types.kString, default="")
    versionNumber = api.AttributeDefinition(input=True, type_=api.types.kInt, default=1)
    thumbnailPath = api.AttributeDefinition(input=True, type_=api.types.kString, default="")
    publishedFileType = api.AttributeDefinition(input=True, type_=api.types.kString, default="")
    dependencyPaths = api.AttributeDefinition(input=True, type_=api.types.kList, default=list())
    sg_fields = api.AttributeDefinition(input=True, type_=api.types.kDict, array=False, default=dict())
    dry_run = api.AttributeDefinition(input=True, type_=api.types.kBool, default=False)

    def execute(self, context):
        engine = self.engine.value()
        if engine is None:
            raise ValueError("No toolkit engine supplied!")
        try:
            import tank
        except ImportError:
            logger.error("shotgun toolkit is not in the current environment")
            raise

        publish_data = {
            "tk": engine.sgtk.value(),
            "context": tank.context.Context.from_dict(engine.sgtk, self.context.value()),
            "comment": self.comment.value(),
            "path": self.path.value(),
            "name": self.name.value(),
            "version_number": self.versionNumber.value(),
            "thumbnail_path": self.thumbnailPath.value(),
            "published_file_type": self.publishedFileType.value(),
            "dependency_paths": self.dependencyPaths.value(),
            "sg_fields": self.fields.value(),
            "dry_run": self.dryRun.value()
        }
        logger.debug("Starting publish {}".format(pprint.pprint(publish_data)))
        return tank.util.register_publish(**publish_data)
