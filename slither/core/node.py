from zoovendor import six
import logging

from slither.core import attribute
from slither.core import graphsearch

logger = logging.getLogger(__name__)


class Context(dict):
    """Subclass of dict to wrap individual nodes attribute types.

    This class is create for every node before it's executed and passed
    to the execute() method.
    """

    def __getattribute__(self, item):
        try:
            return self["inputs"][item]
        except KeyError:
            try:
                return self["outputs"][item]
            except KeyError:
                return super(Context, self).__getattribute__(item)

    def __setattr__(self, key, value):
        try:
            self["inputs"][key] = value
        except KeyError:
            try:
                self["outputs"][key] = value
            except KeyError:
                pass

    def serialize(self):
        attrData = {"outputs": {}, "inputs": {},
                    "name": self["name"]}
        for attrName, attrValue in self["outputs"].items():
            attrData["outputs"][attrName] = attrValue.value()
        for attrName, attrValue in self["inputs"].items():
            attrData["inputs"][attrName] = attrValue.value()
        return attrData

    @staticmethod
    def extractContextDataFromNode(node):
        attrData = {"outputs": {}, "inputs": {}}
        for attr in node.attributes:
            if attr.isInput():
                attrData["inputs"][attr.name()] = attr.value()
            else:
                attrData["outputs"][attr.name()] = attr.value()
        attrData["name"] = node.name
        return attrData

    @classmethod
    def fromExtractData(cls, contextData):
        attrData = {"outputs": {}, "inputs": {}}
        for attrName, attrValue in contextData["outputs"].items():
            attrData["outputs"][attrName] = ContextAttr(attrValue)
        for attrName, attrValue in contextData["inputs"].items():
            attrData["inputs"][attrName] = ContextAttr(attrValue)
        attrData["name"] = contextData["name"]
        return cls(**attrData)

    @classmethod
    def fromNode(cls, node):
        attrData = {"outputs": {}, "inputs": {}}
        for attr in node.attributes:
            if attr.isInput():
                attrData["inputs"][attr.name()] = ContextAttr(attr.value())
            else:
                attrData["outputs"][attr.name()] = ContextAttr(attr.value())
        attrData["name"] = node.name
        return cls(**attrData)


class ContextAttr(object):
    def __init__(self, value):
        self._value = value

    def value(self):
        return self._value

    def setValue(self, value):
        self._value = value


class NodeMeta(type):
    # @staticmethod
    def __new__(cls, className, bases, classDict):
        newClassDict = {}
        for name, attr in classDict.items():
            if isinstance(attr, attribute.AttributeDefinition):
                attr.setName(name)
                attr.internal = True
                newName = '_{}'.format(name)
                newClassDict[newName] = attr
            else:
                newClassDict[name] = attr

        return super(NodeMeta, cls).__new__(cls, className, bases, newClassDict)


class BaseNode(object):
    Type = ""
    category = ""
    tags = []
    documentation = ""

    @classmethod
    def create(cls, info, graph, proxyClass):
        """
        :param info:
        :type info:
        :param graph:
        :type graph:
        :param proxyClass:
        :type proxyClass:
        :return:
        :rtype: :class:`BaseNode` or :class:`DependencyNode`
        """
        name = info["name"]
        node = cls(name, graph, proxyClass)
        node.properties = info.get("properties", {})
        node.nodeUI = info.get("nodeUI", {})
        node.isLocked = info.get("locked", False)
        node.tags = info.get("tags", [])
        node.documentation = info.get("documentation", "")
        node.category = info.get("category", "misc")
        node.Type = info.get("type", "")
        return node

    def __init__(self, name, graph, proxyClass):
        self.graph = graph
        self.name = name
        self.proxyCls = proxyClass
        self.isLocked = False
        self.isInternal = False
        self._parent = None
        self.properties = {}
        self.nodeUI = {}

    @staticmethod
    def isCompound():
        """StaticMethod, Returns whether or not this node is a compound.
        :return: True if a compound.
        :rtype: bool
        """
        return False

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.name)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, node):
        if self._parent != node:
            self._parent = node

    def depth(self):
        index = 0
        if self.parent:
            index += self.parent.depth + 1
        return index

    def siblings(self):
        """Finds and returns all the siblings nodes under the node parent

        :return:
        :rtype: list(Basenode instance)
        """
        nodes = []
        if self.parent:
            for i in self.parent:
                if i != self:
                    nodes.append(i)
        return nodes

    def type(self):
        """Returns the type of this node
        :rtype: string
        """
        return self.Type

    def setName(self, name):
        """Sets the name of the node if the name already exists in the graph then a number will be append
        :param name: The name of the node.
        :type name: str
        :rtype: str
        """
        oldName = self.name
        if oldName != name:
            self.name = name
            self.graph.application.events.emit(self.graph.application.events.nodeNameChanged,
                                               sender=self,
                                               node=self,
                                               oldName=name,
                                               name=name)

        return self.name

    def fullName(self):
        """Returns the full path name of the node eg. |parent|currentNode
        :rtype str
        """
        if self.parent:
            return "|".join([self.parent.fullName(), self.name])
        return self.name

    def serialize(self):
        data = {"name": self.name,
                "type": self.Type,
                "category": self.category,
                "documentation": self.documentation,
                "tags": self.tags,
                "nodeUI": self.nodeUI,
                "properties": self.properties
                }
        if self.parent is not None:
            data["parent"] = self.parent.name
        return data

    def deserialize(self, data):
        self.nodeUI.update(data.get("nodeUI", {}))
        self.properties.update(data.get("properties", {}))
        return {}


@six.add_metaclass(NodeMeta)
class DependencyNode(BaseNode):
    @classmethod
    def create(cls, info, graph, proxyClass):
        n = super(DependencyNode, cls).create(info, graph, proxyClass)
        for name, _in, _out in (("execInput", True, False), ("execOutput", False, True)):
            execDef = attribute.AttributeDefinition(name=name,
                                                    input=_in,
                                                    output=_out,
                                                    type_=graph.application.registry.dataTypeClass("kExec"),
                                                    default=None,
                                                    required=False, array=False,
                                                    doc="",
                                                    internal=True,
                                                    exec_=True,
                                                    serializable=True)
            n.createAttribute(execDef)
        for attr in info.get("attributes", []):
            if n.hasAttribute(attr["name"]):
                continue
            attrDef = attribute.AttributeDefinition(name=attr["name"],
                                                    input=attr.get("input", False),
                                                    output=attr.get("output", False),
                                                    type_=graph.application.registry.dataTypeClass(attr["type"]),
                                                    default=attr.get("default"),
                                                    required=attr.get("required", False), array=attr["array"],
                                                    doc=attr.get("documentation", ""),
                                                    internal=attr.get("internal", False))
            n.createAttribute(attrDef)
        return n

    def __init__(self, name, graph, proxyClass):
        self.attributes = []
        super(DependencyNode, self).__init__(name, graph, proxyClass)

    def __getattr__(self, name):
        """Returns the attribute on the current node if it exists.

        :param name: The name of the attribute
        :type name: str
        :rtype: Attribute
        """
        attr = self.attribute(name)
        if attr is not None:
            return attr
        return super(DependencyNode, self).__getattribute__(name)

    def attribute(self, name):
        shortName = name.split("|")[-1]
        for attr in self.iterAttributes():
            if attr.name() == shortName:
                return attr

    def addAttribute(self, attribute):
        if attribute not in self.attributes:
            self.attributes.append(attribute)
            self.graph.application.events.emit(self.graph.application.events.attributeCreated,
                                               sender=self,
                                               node=self, attribute=attribute)
            return True
        logger.warning("Couldn't create attribute: node-{}: attribute-{}".format(self.node.name(), attribute.name()))
        return False

    def createAttribute(self, attributeDefinition):
        if self.hasAttribute(attributeDefinition.name):
            logger.error("Can't create attribute: {} because it already exists".format(attributeDefinition.name))
            raise ValueError("Name -> {} already exists".format(attributeDefinition.name))
        logger.debug("Creating Attribute: {} on node: {}".format(attributeDefinition.name,
                                                                 self.name))
        if attributeDefinition.array:
            newAttribute = attribute.ArrayAttribute(attributeDefinition, node=self)
        elif attributeDefinition.compound:
            newAttribute = attribute.CompoundAttribute(attributeDefinition, node=self)
        elif attributeDefinition.exec_:
            newAttribute = attribute.ExecAttribute(attributeDefinition, node=self)
        else:
            newAttribute = attribute.Attribute(attributeDefinition, node=self)

        self.addAttribute(newAttribute)
        return newAttribute

    def removeAttribute(self, name):
        for i in range(len(self.attributes)):
            attr = self.attributes[i]
            if attr.name() == name:
                attr.delete()
                del self.attributes[i]
                return True
        return False

    def hasAttribute(self, name):
        return True if self.attribute(name) else False

    def inputs(self):
        return list(self.iterInputs())

    def attributeCount(self):
        return len(self.attributes)

    def iterAttributes(self):
        return iter(self.attributes)

    def outputs(self):
        return list(self.iterOutputs())

    def iterInputs(self):
        for i in self.attributes:
            if i.isInput():
                yield i

    def iterOutputs(self):
        for i in self.attributes:
            if i.isOutput():
                yield i

    def hasOutputs(self):
        for attr in self.iterAttributes():
            if attr.isOutput():
                return True
        return False

    def hasInputs(self):
        for attr in self.iterAttributes():
            if attr.isInput():
                return True
        return False

    def upstreamNodes(self):
        nodes = []
        for input_ in self.iterInputs():
            for upstream in input_.upstream():
                node = upstream.node
                if node is not None:
                    nodes.append(node)
        return nodes

    def downStreamNodes(self):
        nodes = []
        visited = set()
        for attr in self.iterOutputs():
            for downstream in attr.downstream():
                dsNode = downstream.node
                if dsNode in visited:
                    continue
                visited.add(dsNode)
                nodes.append(dsNode)
        return nodes

    def disconnectAll(self):
        for attr in self.iterAttributes():
            attr.disconnect()

    def copyOutputData(self, outputs):
        """Copies the output data on to this nodes output values.

        :param outputs:
        :type outputs:
        :return:
        :rtype:
        """
        for name, value in iter(outputs.items()):
            attr = self.attribute(name)
            if attr is not None:
                attr.setValue(value)

    def serialize(self):
        data = super(DependencyNode, self).serialize()
        attrs = []
        for attr in self.attributes:
            attrInfo = attr.serialize()
            if attrInfo:
                attrs.append(attrInfo)
        data["attributes"] = attrs
        return data

    def deserialize(self, data):
        super(DependencyNode, self).deserialize(data)
        for attr in data["attributes"]:
            attr = dict(attr)
            currentAttr = self.attribute(attr["name"].split("|")[-1])
            if currentAttr is not None:
                currentAttr.deserialize(attr)
            else:
                # temp solution
                attr["type_"] = self.graph.dataType(attr["type_"])
                self.createAttribute(attributeDefinition=attribute.AttributeDefinition(**attr))
        return {}


class Comment(BaseNode):
    Type = "comment"
    documentation = "A single node with a description"

    def __init__(self, name, graph, proxyClass):
        super(Comment, self).__init__(name, graph, proxyClass)
        self.title = ""
        self.comment = ""

    def serialize(self):
        data = super(Comment, self).serialize()
        data["comment"] = self.comment
        data["title"] = self.title


class Pin(DependencyNode):
    Type = "pin"


class ComputeNode(DependencyNode):
    """Node which has a computation operation
    """

    def __init__(self, name, graph, proxyClass):
        super(ComputeNode, self).__init__(name, graph, proxyClass)
        self._progress = 0
        self._dirty = False

    #
    # def process(self, context):
    #     fullName = self.fullName()
    #     start = timeit.default_timer()
    #     try:
    #         logger.debug("Processing node: {}".format(fullName),
    #                      extra={"context": context})
    #         self.progress = 0
    #         self.validate(context)
    #         self.compute(context)
    #         self.progress = 100
    #     except Exception:
    #         self.progress = 0
    #         logger.error("Failed to execute Node: {}".format(fullName),
    #                      exc_info=True)
    #         raise
    #     logger.debug("Finished executing Node: {}, running time: {}".format(fullName,
    #                                                                         timeit.default_timer() - start))
    #     self.setDirty(False)

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value

    def dirty(self):
        return self._dirty

    def setDirty(self, state, propagate=True):
        if self._dirty == state:
            return
        self._dirty = state
        logger.debug("Node: {},  dirty state changed, '{}'".format(self.fullName(), str(state)))
        self.graph.application.events.emit(self.graph.application.events.nodeDirtyChanged, sender=self,
                                           node=self, state=state)
        # if we setting to a dirty state and we need to propagate
        # then loop the downstream nodes and set their state
        if state and propagate:
            for dependent in self.downStreamNodes():
                dependent.setDirty(state, propagate)


class Compound(ComputeNode):
    """The Compound class encapsulates a set of child nodes, which can include other compounds.
    We provide methods to query the children nodes of the current compound.
    """
    Type = "compound"

    def __init__(self, name, graph, proxyClass):
        """
        :param name: The name that this node will have, if the name already exist a number we be appended.
        :type name: str
        """
        super(Compound, self).__init__(name, graph=graph, proxyClass=proxyClass)
        self.children = []
        if not self.nodeUI.get("label"):
            self.nodeUI["label"] = self.Type

    @staticmethod
    def isCompound():
        return True

    def __len__(self):
        """returns the number of child nodes for this compound

        :return: int
        """
        return len(self.children)

    def __iter__(self):
        """Returns a generator of the child nodes

        :return: generator
        """
        return iter(self.children)

    def __add__(self, other):
        """Adds the nodes from one compound to this one

        :param other: Compound
        """
        if isinstance(other, Compound):
            for child in other:
                self.addChild(child)

    def __sub__(self, other):
        if isinstance(other, Compound):
            for child in other:
                if child in self.children:
                    self.children.remove(child)

    def __contains__(self, item):
        return item in self.children

    def child(self, name):
        for child in self.children:
            if child.name == name:
                return child
            elif child.isCompound():
                return child.child(name)

    def addChild(self, child):
        if child not in self.children:
            self.children.append(child)
            parent = child.parent
            if parent and parent.isCompound():
                parent.removeChild(child)
            child.parent = self
            return True
        return False

    def createNode(self, name, type_):
        return self.graph.createNode(name, type_, parent=self)

    def removeChild(self, child):
        return self.graph.removeNode(child, parent=self)

    def clear(self):
        for child in self.children:
            self.removeChild(child)
        self.children = []

    def remove(self):
        if self.isLocked or self.isInternal:
            return False
        par = self.parent
        if par is not None:
            self.clear()
            par.removeChild(self)
            return True
        return False

    def hasChild(self, name):
        return any(i.name == name for i in self)

    def hasChildren(self):
        return len(self.children) > 0

    def topologicalOrder(self):
        return graphsearch.topologicalOrder(self.children)

    def serialize(self):
        data = super(Compound, self).serialize()
        for child in self.children:
            childInfo = child.serialize()
            if childInfo:
                data.setdefault("children", []).append(childInfo)
        return data

    def deserialize(self, data, includeChildren=True):
        super(Compound, self).deserialize(data)
        newChildren = {}
        if not includeChildren:
            return newChildren
        for child in data.get("children", []):
            newNode = self.createNode(child["name"], type_=child["type"])
            if newNode is None:
                raise ValueError("Failed to create node: {}".format(child["name"]))
            for nName, n in newNode.deserialize(child).items():
                newChildren[nName] = n
            newChildren[child["name"]] = newNode
        return newChildren
