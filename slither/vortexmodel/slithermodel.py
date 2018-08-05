"""
Qt model for the vortex ui which bind slithers core engine and vortex GUI.

FYI: Currently this is being prototyped so it pulls and pushes directly to the core without an undo.

"""
import logging
import pprint
from functools import partial
from slither import api
from qt import QtGui, QtWidgets
from vortex.ui.graphics import graphicsdatamodel
from vortex.ui import application
import attributewidgets
logger = logging.getLogger(__name__)

ATTRIBUTETYPEMAP = {'Quaternion': QtGui.QColor(126.999945, 24.999944999999997, 24.999944999999997),
                    'color': QtGui.QColor(22.999980000000015, 255, 255),
                    'matrix4': QtGui.QColor(174.99987000000002, 130.00001999999998, 114.99990000000001),
                    'multi': QtGui.QColor(255, 255, 255),
                    'vector2D': QtGui.QColor(147.000105, 102.0, 156.000075),
                    'vector3D': QtGui.QColor(184.99994999999998, 126.999945, 184.99994999999998),
                    bool: QtGui.QColor(38.00010000000001, 73.99998000000001, 114.000045),
                    dict: QtGui.QColor(204.0, 127.5, 163.20000000000002),
                    float: QtGui.QColor(133.000095, 102.0, 147.99996000000002),
                    int: QtGui.QColor(133.000095, 102.0, 147.99996000000002),
                    list: QtGui.QColor(56.000040000000006, 47.99992500000001, 45.00010500000001),
                    str: QtGui.QColor(244.9999965, 214.999935, 59.99997)
                    }
ATTRIBUTE_DISCONNECTED_COLOR = QtGui.QColor(25, 25, 25)
NODECOLORMAP = {}


class Application(application.UIApplication):
    def __init__(self, uiConfig):
        app = api.initialize()
        super(Application, self).__init__(uiConfig, app)
        self.currentModel = SlitherUIObject(app.root, self.config)
        self.models[self.currentModel.text()] = self.currentModel

    def initialize(self):
        self.onNewNodeRequested.emit({"model": self.currentModel,
                                      "newTab": True})
        self._apiApplication.events.addCallback(self._apiApplication.events.kNodeCreated, self.uiNodeForCore)
        self._apiApplication.events.addCallback(self._apiApplication.events.kSelectedChanged, self.onSelectionChangedEvent)
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

    def uiNodeForCore(self, node):
        """Called by the core api to added node to current model

        :param node:
        :type node:
        :return:
        :rtype:
        """

        self.onNewNodeRequested.emit({"model": SlitherUIObject(node, self.config, parent=self.currentModel),
                                      "newTab": node.isCompound()})

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
        logger.debug(pprint.pformat(self.currentModel.slitherNode.serialize()))

    def createContextMenu(self, objectModel):
        if isinstance(objectModel, SlitherUIObject) and objectModel.isCompound():
            menu = QtWidgets.QMenu()
            import uuid
            # note: this is temp, should run through a dialog
            menu.addAction("Create Attribute", partial(objectModel.createAttribute, str(uuid.uuid4()), str, "output"))
            return menu

    def onSelectionChangedEvent(self, node, state=False):
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

    def _onConnectionAdded(self, sender, source, destination, sourceNode, destinationNode):
        if not self.isCompound():
            destinationNodeModel = None
            destinationAttr = None
            for i in self.parentObject().children():
                if i.slitherNode == destinationNode:
                    destinationNodeModel = i
                    for attr in i.attributes():
                        if attr.internalAttr == destination:
                            destinationAttr = attr
                            break
                    break
            sourceAttr = None
            for attr in self.attributes():
                if attr.internalAttr == source:
                    sourceAttr = attr
                    break
            if destinationNodeModel and sourceAttr and destinationAttr:
                self.addConnectionSig.emit(self, destinationNodeModel,
                                           sourceAttr, destinationAttr)

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

    def secondaryText(self):
        return self.slitherNode.type()

    def toolTip(self):
        return self.slitherNode.documentation

    def attributes(self, inputs=True, outputs=True):
        if not self._attributes:
            attrs = []
            if inputs:
                attrs.extend([AttributeModel(i, self) for i in self.slitherNode.inputs()])
            if outputs:
                attrs.extend([AttributeModel(i, self) for i in self.slitherNode.outputs()])
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

        # mainWidget =
        # for i in self.attributes(True, False):
        #     Type = i.internalAttr.type().Type
        #     print Type
        #     if isinstance(Type, int):
        #         print "int"
        #     elif Type is float:
        #         print "float"
        # ATTRIBUTETYPEMAP = {'Quaternion': Vector,
        #                     'color': QtGui.QColor(22.999980000000015, 255, 255),
        #                     'matrix4': Matrix,
        #                     'vector2D': Vector,
        #                     'vector3D': Vector,
        #                     bool: QtWidgets.QCheckBox,
        #                     dict: QtGui.QColor(204.0, 127.5, 163.20000000000002),
        #                     float: NumericAttributeWidget,
        #                     int: NumericAttributeWidget,
        #                     list: QtGui.QColor(56.000040000000006, 47.99992500000001, 45.00010500000001),
        #                     str: stringEdit
        #                     }
        print "attyr"

class AttributeModel(graphicsdatamodel.AttributeModel):
    def __init__(self, slitherAttribute, objectModel):
        super(AttributeModel, self).__init__(objectModel)
        self.internalAttr = slitherAttribute

    def text(self):
        return self.internalAttr.name()

    def setText(self, text):
        self.internalAttr.setName(str(text))

    def toolTip(self):
        return self.internalAttr.__doc__

    def isConnected(self):
        return self.internalAttr.hasUpstream()

    def canAcceptConnection(self, plug):
        return self.internalAttr.canConnect(plug.internalAttr)

    def createConnection(self, attribute):
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

    def toolTip(self):
        return self.internalAttr.definition.documentation()

    def isInput(self):
        return self.internalAttr.isInput()

    def isOutput(self):
        return self.internalAttr.isOutput()

    def itemEdgeColor(self):
        attr = self.internalAttr
        Map = ATTRIBUTETYPEMAP.get(attr.type().Type)
        if Map:
            return Map
        return super(AttributeModel, self).itemEdgeColor()

    def itemColour(self):
        attr = self.internalAttr
        if attr.isInput() and not attr.upstream:
            return ATTRIBUTE_DISCONNECTED_COLOR
        Map = ATTRIBUTETYPEMAP.get(attr.type().Type)
        if Map:
            return Map
        return super(AttributeModel, self).itemColour()
