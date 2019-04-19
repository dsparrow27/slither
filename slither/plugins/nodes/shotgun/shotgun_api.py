from slither import api


class ShotgunConnection(api.ComputeNode):
    Type = "shotgunConnection"
    category = "shotgun"
    documentation = "Creates and returns a shotgun connection instance"
    apiScript = api.AttributeDefinition(isInput=True, type_=api.types.kString, array=False, default="")
    apiKey = api.AttributeDefinition(isInput=True, type_=api.types.kString, default="")
    host = api.AttributeDefinition(isInput=True, type_=api.types.kString, default="")
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kShotgun, array=False, default=None)

    def execute(self):
        import shotgun_api3
        apihandle = shotgun_api3.Shotgun(
            self.host.value(),
            script_name=self.apiScript.value(),
            api_key=self.apiKey.value(),
            connect=False
        )
        self.output.setValue(apihandle)


class ShotgunFind(api.ComputeNode):
    type = "shotgunFind"
    category = "shotgun"
    documentation = "Calls 'find' method on the shotgun instance and returns the result as an attribute array"
    shotgunConnection = api.AttributeDefinition(isInput=True, type_="shotgun", array=False, default=None)
    entityType = api.AttributeDefinition(isInput=True, type_=api.types.kString, array=False, default="")
    filters = api.AttributeDefinition(isInput=True, type_=api.types.kList, array=True, default=list())
    fields = api.AttributeDefinition(isInput=True, type_=api.types.kList, array=True, default=list())
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kList, array=True, default=list())

    def execute(self):
        self.output = self.shotgunConnection.value().find(self.entityType.value(),
                                                          list(self.filters.value()),
                                                          list(self.fields.value()))


class ShotgunFindOne(api.ComputeNode):
    Type = "shotgunFindOne"
    category = "shotgun"
    documentation = "Calls 'find_one' method on the shotgun instance and returns the result as an attribute dict"
    shotgunConnection = api.AttributeDefinition(isInput=True, type_=api.types.kShotgun, array=False, default=None)
    entityType = api.AttributeDefinition(isInput=True, type_=api.types.kString, array=False, default="")
    filters = api.AttributeDefinition(isInput=True, type_=api.types.kList, array=True, default=list())
    fields = api.AttributeDefinition(isInput=True, type_=api.types.kList, array=True, default=list())
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kDict, array=False, default=dict())

    def execute(self):
        self.output = self.shotgunConnection.value().find_one(self.entityType.value(),
                                                              list(self.filters.value()),
                                                              list(self.fields.value()))
