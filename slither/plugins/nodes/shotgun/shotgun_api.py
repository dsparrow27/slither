from slither import api


class ShotgunConnection(api.ComputeNode):
    Type = "shotgunConnection"
    category = "shotgun"
    documentation = "Creates and returns a shotgun connection instance"
    apiScript = api.AttributeDefinition(input=True, type_=api.types.kString, array=False, default="")
    apiKey = api.AttributeDefinition(input=True, type_=api.types.kString, default="")
    host = api.AttributeDefinition(input=True, type_=api.types.kString, default="")
    output = api.AttributeDefinition(output=True, type_=api.types.kShotgun, array=False, default=None)

    def execute(self, context):
        import shotgun_api3
        apihandle = shotgun_api3.Shotgun(
            context.host.value(),
            script_name=context.apiScript.value(),
            api_key=context.apiKey.value(),
            connect=False
        )
        context.output.setValue(apihandle)


class ShotgunFind(api.ComputeNode):
    type = "shotgunFind"
    category = "shotgun"
    documentation = "Calls 'find' method on the shotgun instance and returns the result as an attribute array"
    shotgunConnection = api.AttributeDefinition(input=True, type_="shotgun", array=False, default=None)
    entityType = api.AttributeDefinition(input=True, type_=api.types.kString, array=False, default="")
    filters = api.AttributeDefinition(input=True, type_=api.types.kList, array=True, default=list())
    fields = api.AttributeDefinition(input=True, type_=api.types.kList, array=True, default=list())
    output = api.AttributeDefinition(output=True, type_=api.types.kList, array=True, default=list())

    def execute(self, context):
        context.output = context.shotgunConnection.value().find(context.entityType.value(),
                                                          list(context.filters.value()),
                                                          list(context.fields.value()))


class ShotgunFindOne(api.ComputeNode):
    Type = "shotgunFindOne"
    category = "shotgun"
    documentation = "Calls 'find_one' method on the shotgun instance and returns the result as an attribute dict"
    shotgunConnection = api.AttributeDefinition(input=True, type_=api.types.kShotgun, array=False, default=None)
    entityType = api.AttributeDefinition(input=True, type_=api.types.kString, array=False, default="")
    filters = api.AttributeDefinition(input=True, type_=api.types.kList, array=True, default=list())
    fields = api.AttributeDefinition(input=True, type_=api.types.kList, array=True, default=list())
    output = api.AttributeDefinition(output=True, type_=api.types.kDict, array=False, default=dict())

    def execute(self, context):
        context.output = context.shotgunConnection.value().find_one(context.entityType.value(),
                                                              context.filters.value(),
                                                              context.fields.value())
