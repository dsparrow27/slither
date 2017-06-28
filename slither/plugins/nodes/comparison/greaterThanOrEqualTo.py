from slither.core import node
from slither.core import attribute


class GreaterThanOrEqualToNode(node.BaseNode):
    value1 = attribute.InputDefinition(float)
    value2 = attribute.InputDefinition(float)
    result = attribute.OutputDefinition(bool)

    def execute(self):
        result = self.value1Plug_ >= self.value2Plug_
        self.result.setValue(result)
