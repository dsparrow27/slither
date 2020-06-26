import copy
import logging
import time

from slither.core import attribute
from slither.core import graphsearch
from slither.core import types
import six
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


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
    @staticmethod
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

    def __init__(self, name, graph):
        self.graph = graph
        self.id = 0
        self.name = name
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
        if self.name != name:
            self.name = name

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
                "id": self.id,
                "category": self.category,
                "documentation": self.documentation,
                "tags": self.tags,
                "nodeUI": self.nodeUI,
                "properties": self.properties
                }
        if self.parent is not None:
            data["parent"] = self.parent.id
        return data

    def deserialize(self, data):
        return {}

@six.add_metaclass(NodeMeta)
class DependencyNode(BaseNode):

    def __init__(self, name, graph):
        self.attributes = []
        super(DependencyNode, self).__init__(name, graph)
        attrDef = attribute.AttributeDefinition(name="Dependencies",
                                                input=True,
                                                output=True,
                                                type_=types.kList,
                                                default=list(),
                                                required=False, array=True,
                                                doc="Node Level dependencies",
                                                internal=True)
        self.createAttribute(attrDef)

        for name, attrDef in iter(self.__class__.__dict__.items()):
            if isinstance(attrDef, attribute.AttributeDefinition):
                self.createAttribute(copy.deepcopy(attrDef))

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

    def createConnection(self, inputAttribute, destinationAttribute):
        return self.graph.createConnection(inputAttribute, destinationAttribute)

    def attribute(self, name):
        for attr in self.iterAttributes():
            if attr.name() == name:
                return attr

    def attributeById(self, attributeId):
        for attr in self.iterAttributes():
            if attr.id == attributeId:
                return attr

    def addAttribute(self, attribute):
        if attribute not in self.attributes:
            attribute.id = 1 if not self.attributes else max(attr.id for attr in self.attributes) + 1
            self.attributes.append(attribute)
            return True
        logger.warning("Couldn't create attribute: node-{}: attrbute-{}".format(self.node.name(), attribute.name()))
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
        else:
            newAttribute = attribute.Attribute(attributeDefinition, node=self)

        name = newAttribute.name()
        className = "_{}".format(name) if not name.startswith("_") else name
        super(DependencyNode, self).__setattr__(className, attributeDefinition)
        self.addAttribute(newAttribute)
        return newAttribute

    def removeAttribute(self, name):
        for i in range(len(self.attributes)):
            attr = self.attributes[i]
            if attr.name() == name:
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
            upstream = input_.upstream
            if upstream is not None:
                nodes.append(upstream.node)
        return nodes

    def downStreamNodes(self):
        nodes = []
        if self.parent:
            children = self.parent.children
            for i in children:
                if self in i.upstreamNodes():
                    nodes.append(i)
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

    def __init__(self, name, graph):
        super(Comment, self).__init__(name, graph)
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

    def __init__(self, name, graph):
        super(ComputeNode, self).__init__(name, graph)
        self._progress = 0
        self._dirty = False

    def process(self, context):
        fullName = self.fullName()
        start = time.clock()
        try:
            logger.debug("Processing node: {}".format(fullName),
                         extra={"context": context})
            self.progress = 0
            self.validate(context)
            self.execute(context)
            self.progress = 100
        except Exception:
            self.progress = 0
            logger.error("Failed to execute Node: {}".format(fullName),
                         exc_info=True)
            raise
        logger.debug("Finished executing Node: {}, running time: {}".format(fullName,
                                                                            time.clock() - start))
        self.setDirty(False)

    def validate(self, context):
        return True

    def execute(self, context):
        pass

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
        # if we setting to a dirty state and we need to propagate
        # then loop the downstream nodes and set their state
        if state and propagate:
            for dependent in self.downStreamNodes():
                dependent.setDirty(state, propagate)


class PythonNode(ComputeNode):
    Type = "python"

    def __init__(self, name, graph):
        super(PythonNode, self).__init__(name, graph)

        attrDef = attribute.AttributeDefinition(name="script",
                                                input=True,
                                                output=True,
                                                type_=types.kString,
                                                default=list(),
                                                required=True,
                                                array=False,
                                                doc="Executable python string")
        self.createAttribute(attrDef)

    def execute(self, context):
        script = context.script
        if not script:
            raise ValueError("")
        script = script.replace(u"\u2029", "\n")
        evalCode = True
        _locals = {"context": context}
        try:
            outputCode = compile(script, "<string>", "eval")
        except SyntaxError:
            evalCode = False
            outputCode = compile(script, "<string>", "exec")
        except Exception:
            raise
        # ok we've compiled the code now exec
        if evalCode:
            try:
                eval(outputCode, globals(), _locals)
            except Exception:
                raise
        else:
            try:
                exec (outputCode, globals(), _locals)
            except Exception:
                raise


class Compound(ComputeNode):
    """The Compound class encapsulates a set of child nodes, which can include other compounds.
    We provide methods to query the children nodes of the current compound.
    """
    Type = "compound"

    def __init__(self, name, graph):
        """
        :param name: The name that this node will have, if the name already exist a number we be appended.
        :type name: str
        """
        super(Compound, self).__init__(name, graph=graph)
        self.children = []

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

    def mutate(self):
        """Special method that allows this node to generate(mutate) other nodes as child nodes this can also contain
        other compounds
        """
        pass

    def child(self, name):
        for child in self:
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
            for nId, n in newNode.deserialize(child).items():
                newChildren[nId] = n
            newChildren[child["id"]] = newNode
        return newChildren
