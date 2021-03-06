import os

from qt import QtWidgets, QtCore
import weakref


class AttributeItemWidget(QtWidgets.QFrame):
    """Class which encapsulates a single attribute widget
    """

    def __init__(self, label, widget, parent=None):
        super(AttributeItemWidget, self).__init__(parent=parent)
        layout = QtWidgets.QFormLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QtWidgets.QLabel(label, parent=self)
        widget.setParent(self)
        layout.addWidget(label)
        layout.addWidget(widget)
        self.setLayout(layout)


class StringWidget(QtWidgets.QLineEdit):
    def __init__(self, model, parent=None):
        super(StringWidget, self).__init__(parent=parent)
        self.model = model


class PathWidget(QtWidgets.QFrame):
    def __init__(self, model, parent=None):
        super(PathWidget, self).__init__(parent=parent)
        self.directory = False
        self.model = model
        self.edit = QtWidgets.QLineEdit(parent=self)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.layout.addWidget(self.edit)
        self.browserBtn = QtWidgets.QPushButton("...", parent=self)
        self.layout.addWidget(self.browserBtn)
        self.browserBtn.clicked.connect(self.onBrowserClicked)
        self.edit.editingFinished.connect(self.onEditChanged)

    def onBrowserClicked(self):
        currentPath = self.edit.text()
        if not os.path.isfile(currentPath):
            currentPath = os.path.dirname(currentPath)
        if not self.directory:
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self, dir=currentPath)
        else:
            fileName = QtWidgets.QFileDialog.getExistingDirectory(parent=self, dir=currentPath)
        if fileName:
            self.edit.setText(fileName)
            self.model.setValue(fileName)

    def onEditChanged(self):
        self.model.setValue(str(self.edit.text()))


class DirectoryWidget(PathWidget):
    def __init__(self, model, parent=None):
        super(DirectoryWidget, self).__init__(model, parent=parent)
        self.directory = True


class NumericAttributeWidget(QtWidgets.QFrame):
    valueChanged = QtCore.Signal(object)

    def __init__(self, model, parent=None):
        super(NumericAttributeWidget, self).__init__(parent=parent)
        self.model = weakref.ref(model)
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(1)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, parent=self)
        self.valueSpinBox = QtWidgets.QSpinBox(parent=self)
        self.valueSpinBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.valueSpinBox.setRange(-100, 100)
        self.valueSpinBox.setSingleStep(1)
        self.valueSpinBox.valueChanged.connect(self.setValue)
        self.slider.valueChanged.connect(self.setValue)
        # self.valueSpinBox.valueChanged.connect(self.valueChanged.emit)
        layout.addWidget(self.slider)
        layout.addWidget(self.valueSpinBox)
        self.setStyleSheet("""
    QSlider::groove:horizontal
    {
        border:none;
    }

    QSlider::sub-page
    {
        background: rgb(164, 192, 2);
    }

    QSlider::add-page
    {
        background: rgb(70, 70, 70);
    }

    QSlider::handle
    {
        background: rgb(164, 192, 2);
        width: 30px;
        margin: -30px 0;
    }
            """)

    def setValue(self, value):
        if self.valueSpinBox.value() != value:
            self.valueSpinBox.setValue(value)
        if self.slider.value() != value:
            self.slider.setValue(value)
        ref = self.model()
        if ref is not None and ref.value() != value:
            ref.setValue(value)
