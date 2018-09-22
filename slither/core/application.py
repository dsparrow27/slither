import uuid

from .registry import NodeRegistry
from .registry import DataTypeRegistry
from slither.core import executor
from blinker import signal
import logging

logger = logging.getLogger(__name__)


class Application(object):
    PARALLELEXECUTOR = 0
    STANDARDEXECUTOR = 1

    def __init__(self):
        self._nodeRegistry = NodeRegistry()
        self._typeRegistry = DataTypeRegistry()
        self._events = ApplicationEvents()
        self._root = None
        self.globals = {}

    def __repr__(self):
        return "<{}>".format(self.__class__.__name__)

    @property
    def events(self):
        return self._events

    @property
    def nodeRegistry(self):
        return self._nodeRegistry

    @property
    def typeRegistry(self):
        return self._typeRegistry

    def dataType(self, typeName):
        return self.typeRegistry.loadPlugin(typeName)

    @property
    def root(self):
        if self._root is not None:
            return self._root
        self._root = self._nodeRegistry.loadPlugin("Compound", name="Root System", application=self)
        # mark the root as internal and locked so it can't be deleted.
        self._root.isLocked = True
        self._root.isInternal = True
        # should emit event
        return self._root

    #:note:: probably shouldn't be doing this crap here
    def createNode(self, name, type_, parent=None):
        exists = self.root.child(name)
        if exists:
            newName = name
            counter = 1
            while self.root.child(newName):
                newName = name + str(counter)
                counter += 1
            name = newName
        newNode = self._nodeRegistry.loadPlugin(type_, name=name, application=self)
        if newNode is not None:
            if parent is None:
                self.root.addChild(newNode)
            elif parent.isCompound():
                parent.addChild(newNode)
            # should emit a event
            self.events.emitCallback(self.events.kNodeCreated, node=newNode)
            return newNode
        # :todo error out

    def execute(self, node, executorType):
        if executorType == Application.PARALLELEXECUTOR:
            logger.debug("Starting execution")
            exe = executor.Parallel()
            exe.execute(node)
            logger.debug("finished")
            return True
        elif executorType == Application.STANDARDEXECUTOR:
            exe = executor.StandardExecutor()
            exe.execute(node)
            return True
        return False


class ApplicationEvents(object):
    kNodeCreated = 0
    kNodeRemoved = 1
    kSelectedChanged = 2

    def __init__(self):
        # {callbackType: {"event": Signal,
        # "ids": {id: func}
        #               }
        # }
        self.callbacks = {}

    def emitCallback(self, callbackType, **kwargs):
        existing = self.callbacks.get(callbackType)
        if existing is None:
            return
        ids = existing["ids"]
        if not ids:
            return
        existing["event"].send(self, **kwargs)

    def addCallback(self, callbackType, func):
        existingCallback = self.callbacks.get(callbackType)

        # we have existing callback for the type so just connect to it
        callbackId = uuid.uuid4()
        if existingCallback is not None:
            existingCallback["event"].connect(func)
            existingCallback["ids"].update({callbackId: func})
        else:
            # no existing callback so create One
            event = signal(callbackType)
            event.connect(func, sender=self)
            self.callbacks[callbackType] = {"event": event,
                                            "ids": {callbackId: func}}
        return callbackId

    def removeCallback(self, callbackId):
        for eventInfo in self.callbacks.values():
            ids = eventInfo["ids"]
            func = ids.get(callbackId)
            if func is not None:
                eventInfo["event"].disconnect(func)
                del ids[callbackId]
                return True
        return True