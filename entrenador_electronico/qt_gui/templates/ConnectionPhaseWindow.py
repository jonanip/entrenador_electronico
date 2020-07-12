from PyQt5 import QtGui, QtWidgets, QtCore
from entrenador_electronico.source.components import BaseComponent


class ParametersDialog(QtWidgets.QDialog):
    def __init__(self, component: BaseComponent, parent=None, *args, **kwargs):
        self.component = component
        super(ParametersDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle(f"{self.component.name} {self.component.id + 1}")
        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        # Creates an horizontal layout for the parameters
        self.h_layout = QtWidgets.QHBoxLayout()
        # Creates a text label
        self.value_label = QtWidgets.QLabel(self.component.short_name)
        self.value_label.setAlignment(QtCore.Qt.AlignRight)
        # Creates a double value spinner
        self.value_textbox = QtWidgets.QDoubleSpinBox()
        self.value_textbox.setMaximum(1E8)
        self.value_textbox.setMinimum(-1E8)
        self.value_textbox.setValue(self.component.component_value)

        self.h_layout.addWidget(self.value_label)
        self.h_layout.addWidget(self.value_textbox)
        self.layout.addLayout(self.h_layout)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        self.component.value = self.value_textbox.value()
        self.close()

