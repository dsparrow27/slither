from qt import QtWidgets, QtCore
import weakref


class AttributeItemWidget(QtWidgets.QFrame):
    """Class which encapsulates a single attribute widget
    """

    def __init__(self, label, widget, parent=None):
        super(AttributeItemWidget, self).__init__(parent=parent)
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QtWidgets.QLabel(label, parent=self)
        widget.setParent(self)
        layout.addWidget(label)
        layout.addWidget(widget)
        self.setLayout(layout)


class NumericAttributeWidget(QtWidgets.QFrame):
    valueChanged = QtCore.Signal(object)

    def __init__(self, model, parent=None):
        super(NumericAttributeWidget, self).__init__(parent=parent)
        self.model = weakref.ref(model)
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.label = QtWidgets.QLabel(self.model().text(), parent=self)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, parent=self)
        self.valueSpinBox = QtWidgets.QSpinBox(parent=self)
        self.valueSpinBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.valueSpinBox.setRange(-100, 100)
        self.valueSpinBox.setSingleStep(1)
        self.valueSpinBox.valueChanged.connect(self.setValue)
        self.slider.valueChanged.connect(self.setValue)
        self.valueSpinBox.valueChanged.connect(self.valueChanged.emit)
        layout.addWidget(self.label)
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
        if ref is not None:
            ref.setValue(value)
