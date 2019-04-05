from slither.core import attribute
from slither.core import node


class ShotgunConnection(node.BaseNode):
    Type = "ShotgunConnection"
    category = "shotgun"
    documentation = "Creates and returns a shotgun connection instance"
    apiScript = attribute.AttributeDefinition(isInput=True, type="str", array=False, default="")
    apiKey = attribute.AttributeDefinition(isInput=True, type="str", default="")
    host = attribute.AttributeDefinition(isInput=True, type="str", default="")
    output = attribute.AttributeDefinition(isOutput=True, type_="shotgun", array=False, default=None)

    def execute(self):
        import shotgun_api3
        apihandle = shotgun_api3.Shotgun(
            self.host.value(),
            script_name=self.apiScript.value(),
            api_key=self.apiKey.value(),
            connect=False
        )
        self.output.setValue(apihandle)


class ShotgunFind(node.BaseNode):
    Type = "ShotgunFind"
    category = "shotgun"
    documentation = "Calls 'find' method on the shotgun instance and returns the result as an attribute array"
    shotgunConnection = attribute.AttributeDefinition(isInput=True, type_="shotgun", array=False, default=None)
    entityType = attribute.AttributeDefinition(isInput=True, type="str", array=False, default="")
    filters = attribute.AttributeDefinition(isInput=True, type="list", array=True, default=list())
    fields = attribute.AttributeDefinition(isInput=True, type="list", array=True, default=list())
    output = attribute.AttributeDefinition(isOutput=True, type="list", array=True, default=list())

    def execute(self):
        self.output = self.shotgunConnection.value().find(self.entityType.value(),
                                                          list(self.filters.value()),
                                                          list(self.fields.value()))


class ShotgunFindOne(node.BaseNode):
    Type = "ShotgunFindOne"
    category = "shotgun"
    documentation = "Calls 'find_one' method on the shotgun instance and returns the result as an attribute dict"
    shotgunConnection = attribute.AttributeDefinition(isInput=True, type_="shotgun", array=False, default=None)
    entityType = attribute.AttributeDefinition(isInput=True, type="str", array=False, default="")
    filters = attribute.AttributeDefinition(isInput=True, type="list", array=True, default=list())
    fields = attribute.AttributeDefinition(isInput=True, type="list", array=True, default=list())
    output = attribute.AttributeDefinition(isOutput=True, type="dict", array=False, default=dict())

    def execute(self):
        self.output = self.shotgunConnection.value().find_one(self.entityType.value(),
                                                              list(self.filters.value()),
                                                              list(self.fields.value()))
