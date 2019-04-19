import math

from slither import api


class Pi(api.ComputeNode):
    Type = "Pi"
    category = "constant"
    documentation = "Pi"
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kBoolean, default=True)

    def execute(self):
        self.output.setValue(math.pi)
