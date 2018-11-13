"""
Qt model for the vortex ui which bind slithers core engine and vortex GUI.

FYI: Currently this is being prototyped so it pulls and pushes directly to the core without an undo.

"""
import logging
import pprint
from functools import partial
from slither import api
from slither.core import executor
from qt import QtGui, QtWidgets
from vortex.ui.graphics import graphicsdatamodel
from vortex.ui import application
import attributewidgets

logger = logging.getLogger(__name__)

ATTRIBUTETYPEMAP = {'Quaternion': {"color": QtGui.QColor(126.999945, 24.999944999999997, 24.999944999999997),
                                   "widget": None},
                    'color': {"color": QtGui.QColor(22.999980000000015, 255, 255)},
                    'matrix4': {"color": QtGui.QColor(174.99987000000002, 130.00001999999998, 114.99990000000001)},
                    'multi': {"color": QtGui.QColor(255, 255, 255)},
                    'vector2D': {"color": QtGui.QColor(147.000105, 102.0, 156.000075)},
                    'vector3D': {"color": QtGui.QColor(184.99994999999998, 126.999945, 184.99994999999998)},
                    "file": {"color": QtGui.QColor(184.99994999999998, 126.999945, 184.99994999999998),
                             "widget": attributewidgets.PathWidget},
                    "directory": {"color": QtGui.QColor(184.99994999999998, 126.999945, 184.99994999999998),
                                  "widget": attributewidgets.DirectoryWidget},
                    bool: {"color": QtGui.QColor(38.00010000000001, 73.99998000000001, 114.000045)},
                    dict: {"color": QtGui.QColor(204.0, 127.5, 163.20000000000002)},
                    float: {"color": QtGui.QColor(133.000095, 102.0, 147.99996000000002),
                            "widget": attributewidgets.NumericAttributeWidget},
                    int: {"color": QtGui.QColor(133.000095, 102.0, 147.99996000000002),
                          "widget": attributewidgets.NumericAttributeWidget},
                    list: {"color": QtGui.QColor(56.000040000000006, 47.99992500000001, 45.00010500000001)},
                    str: {"color": QtGui.QColor(244.9999965, 214.999935, 59.99997),
                          "widget": attributewidgets.StringWidget}
                    }
ATTRIBUTE_DISCONNECTED_COLOR = QtGui.QColor(2, 25, 25)
NODECOLORMAP = {}


class Application(application.UIApplication):
    def __init__(self, uiConfig):
        app = api.currentInstance
        super(Application, self).__init__(uiConfig, app)
        self.currentModel = SlitherUIObject(app.root, self.config)
        self.models[self.currentModel.text()] = self.currentModel

    def initialize(self):
        self.onNewNodeRequested.emit({"model": self.currentModel,
                                      "newTab": True})
        self._apiApplication.events.addCallback(self._apiApplication.events.kNodeCreated, self.uiNodeForCore)
        self._apiApplication.events.addCallback(self._apiApplication.events.kSelectedChanged,
                                                self.onSelectionChangedEvent)
        self._apiApplication.events.addCallback(self._apiApplication.events.kNodeRemoved, self.onNodeRemoved)
        # self._apiApplication.events.addCallback(self._apiApplication.events.kConnectionAdded, self.onConnectionAdded)
        # self._apiApplication.events.addCallback(self._apiApplication.events.kConnectionRemoved, self.onConnectionRemoved)

    def onConnectionAdded(self, sender, source, destination, sourceNode, destinationNode):
        sNode = None
        destNode = None
        for child in self.currentModel.children():
            if child.slitherNode == sourceNode:
                source = child
            elif child.slitherNode == destinationNode:
                destination = child
            if sNode and destNode:
                break

        if sNode and destination:
            sourceAttr = sNode.attribute(source.name)
            destinationAttr = destNode.attribute(destination.name)
            sourceAttr.createConnection(destinationAttr)
            self.onConnectionAddedRequested.emit(sourceAttr, destinationAttr)

    def onNodeRemoved(self, event, node):
        for child in self.currentModel.children():
            if child.slitherNode == node:
                self.onNodeDeleteRequested.emit(child)
                return True

    def onConnectionRemoved(self, sender, source, destination, sourceNode, destinationNode):
        sNode = None
        destNode = None
        for child in self.currentModel.children():
            if child.slitherNode == sourceNode:
                source = child
            elif child.slitherNode == destinationNode:
                destination = child
            if sNode and destNode:
                break

        if sNode and destination:
            sourceAttr = sNode.attribute(source.name)
            destinationAttr = destNode.attribute(destination.name)
            sourceAttr.deleteConnection(destinationAttr)
            self.onConnectionDeleteRequested.emit(sourceAttr, destinationAttr)

    def uiNodeForCore(self, event, node):
        """Called by the core api to added node to current model

        :param node:
        :type node:
        :return:
        :rtype:
        """

        self.onNewNodeRequested.emit({"model": SlitherUIObject(node, self.config, parent=self.currentModel),
                                      "newTab": False})

    def onNodeCreated(self, Type):
        name = Type
        self._apiApplication.createNode(name, Type, parent=self.currentModel.slitherNode)

    def registeredNodes(self):
        """

        :return: category: name
        :rtype: dict
        """

        return dict([(k, v.category) for k, v in self._apiApplication.nodeRegistry.plugins.items()])

    def customToolbarActions(self, parent):
        act = parent.addAction("Execute")
        act.triggered.connect(self.onExecute)

    def onExecute(self):
        # note: temp
        exe = executor.StandardExecutor()
        exe.execute(self.currentModel.slitherNode)
        logger.debug(pprint.pformat(self.currentModel.slitherNode.serialize()))

    def createContextMenu(self, objectModel):
        if isinstance(objectModel, SlitherUIObject) and objectModel.isCompound():
            menu = QtWidgets.QMenu()
            import uuid
            # note: this is temp, should run through a dialog
            menu.addAction("Create Attribute", partial(objectModel.createAttribute, str(uuid.uuid4()), str, "output"))
            return menu

    def onSelectionChangedEvent(self, event, **kwargs):
        node = kwargs["node"]
        state = kwargs["state"]
        for child in self.currentModel.children():
            if child.slitherNode == node:
                self.onSelectionChanged.emit(child, state)


class SlitherUIObject(graphicsdatamodel.ObjectModel):

    def __init__(self, slitherNode, config, parent=None):
        super(SlitherUIObject, self).__init__(config, parent)
        self.slitherNode = slitherNode

        if self.isCompound():
            self._children = [SlitherUIObject(slitherNode=i, config=self.config, parent=self) for i in
                              slitherNode.children]
        else:
            self._children = []
        self._attributes = []
        self.slitherNode.events.addCallback(self.slitherNode.events.kAddConnection, self._onConnectionAdded)
        self.slitherNode.events.addCallback(self.slitherNode.events.kRemoveConnection,
                                            self.onConnectionRemoved)

    def onConnectionRemoved(self, event, **kwargs):
        sourceNodeModel = self._childBySlither(kwargs["sourceNode"])
        sourceAttributeModel = self.attribute(kwargs["source"].name())
        destinationModel = self._childBySlither(kwargs["destinationNode"])
        if sourceNodeModel and sourceAttributeModel:
            self.removeConnectionSig.emit(sourceAttributeModel,
                                          destinationModel.attribute(kwargs["destination"].name()))

    def _onConnectionAdded(self, event, **kwargs):
        sourceNodeModel = self._childBySlither(kwargs["sourceNode"])
        sourceAttributeModel = sourceNodeModel.attribute(kwargs["source"].name())
        destinationModel = self._childBySlither(kwargs["destinationNode"])
        destinationAttributeModel = destinationModel.attribute(kwargs["destination"].name())
        if sourceAttributeModel and destinationAttributeModel:
            self.addConnectionSig.emit(sourceAttributeModel, destinationAttributeModel)

    def _childBySlither(self, slitherNode):
        if slitherNode == self.slitherNode:
            return self
        parent = self._parent
        if parent is None:
            return self
        elif parent.slitherNode == slitherNode:
            return parent
        for i in iter(parent.children()):
            if i.slitherNode == slitherNode:
                return i

    def isSelected(self):
        return self.slitherNode.selected

    def setSelected(self, value):
        self.slitherNode.selected = value

    def isCompound(self):
        return self.slitherNode.isCompound()

    def category(self):
        return self.slitherNode.category

    def children(self):
        return self._children

    def __hash__(self):
        return id(self)

    def text(self):
        return self.slitherNode.name

    def setText(self, value):
        self.slitherNode.name = value
        return self.slitherNode.name
    def secondaryText(self):
        return self.slitherNode.type()

    def toolTip(self):
        return self.slitherNode.documentation

    def attributes(self, inputs=True, outputs=True, attributeVisLevel=0):
        attrs = []
        if attributeVisLevel == self.ATTRIBUTE_VIS_LEVEL_ZERO:
            attrs = []
        # display only connected
        elif attributeVisLevel == self.ATTRIBUTE_VIS_LEVEL_ONE:
            for attr in self.slitherNode.iterAttributes():
                if inputs and attr.isInput() and attr.hasUpstream():
                    attrs.append(AttributeModel(attr, self))
                    continue
                if outputs and attr.isOutput():
                    attrs.append(AttributeModel(attr, self))
        else:
            for attr in self.slitherNode.iterAttributes():
                if inputs and attr.isInput():
                    attrs.append(AttributeModel(attr, self))
                    continue
                if outputs and attr.isOutput():
                    attrs.append(AttributeModel(attr, self))
        self._attributes = attrs
        return self._attributes

    def canCreateAttributes(self):
        if self.isCompound():
            return True
        return False

    def createAttribute(self, name, Type, IOType="output"):
        if not self.canCreateAttributes():
            return
        # temp, should be constants
        if IOType == "output":
            attrDef = api.OutputDefinition(Type)
        else:
            attrDef = api.InputDefinition(Type)
        attrDef.name = name
        self.slitherNode.createAttribute(attrDef)

    def deleteAttribute(self, attribute):
        pass

    def deleteChild(self, child):
        if self.isCompound():
            result = self.slitherNode.removeChild(child.slitherNode)
            if result:
                self._children.remove(child)
                return True
        return False

    def delete(self):
        parent = self.parentObject()
        if parent is not None:
            return parent.deleteChild(self)
        return False

    def contextMenu(self, menu):
        pass

    def attributeWidget(self, parent):
        # todo: mostly temp so we'll need a more ideal solution maybe json?
        parentWidget = QtWidgets.QWidget(parent)
        layout = QtWidgets.QFormLayout(parent=parentWidget)
        parentWidget.setLayout(layout)
        for i in self.attributes(True, False):
            if not i.isInput():
                continue
            Type = i.internalAttr.type().Type
            typeInfo = ATTRIBUTETYPEMAP.get(Type)
            if typeInfo:
                widget = typeInfo.get("widget")
                if widget is not None:
                    widget = widget(i, parent=parentWidget)
                    layout.addRow(i.text(), widget)
        return parentWidget


class AttributeModel(graphicsdatamodel.AttributeModel):
    def __init__(self, slitherAttribute, objectModel):
        super(AttributeModel, self).__init__(objectModel)
        self.internalAttr = slitherAttribute

    def __ne__(self, other):
        return self.internalAttr != other.internalAttr

    def __eq__(self, other):
        return self.internalAttr != other.internalAttr

    def __hash__(self):
        return hash(self.internalAttr.name())

    def text(self):
        return self.internalAttr.name()

    def setText(self, text):
        self.internalAttr.setName(str(text))

    def toolTip(self):
        return self.internalAttr.definition.documentation()

    def isArray(self):
        return self.internalAttr.definition.isArray

    def isCompound(self):
        return self.internalAttr.definition.isCompound

    def isConnected(self):
        return self.internalAttr.hasUpstream()

    def canAcceptConnection(self, plug):
        return self.internalAttr.canConnect(plug.internalAttr)

    def createConnection(self, attribute):
        if not self.canAcceptConnection(attribute):
            return False
        if self.internalAttr.isInput():
            self.internalAttr.connectUpstream(attribute.internalAttr)
        else:
            attribute.internalAttr.connectUpstream(self.internalAttr)
        return True

    def deleteConnection(self, attribute):
        if self.internalAttr.isConnectedTo(attribute.internalAttr):
            if self.internalAttr.isInput():
                self.internalAttr.disconnect()
            else:
                attribute.internalAttr.disconnect()
            return True
        return False

    def isInput(self):
        return self.internalAttr.isInput()

    def isOutput(self):
        return self.internalAttr.isOutput()

    def setValue(self, value):
        self.internalAttr.setValue(value)

    def value(self):
        return self.internalAttr.value()

    def itemEdgeColor(self):
        return ATTRIBUTE_DISCONNECTED_COLOR

    def itemColour(self):
        attr = self.internalAttr
        # if attr.upstream is None:
        #     return ATTRIBUTE_DISCONNECTED_COLOR
        Map = ATTRIBUTETYPEMAP.get(attr.type().Type)
        if Map:
            return Map["color"]
        return super(AttributeModel, self).itemColour()
