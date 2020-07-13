from PyQt5 import QtGui, QtWidgets, QtCore
from entrenador_electronico.source.components import BaseComponent
from entrenador_electronico.source.components.Components import Components
from entrenador_electronico.source.ConnectionPhase import ConnectionPhase

class ComponentIcon(QtWidgets.QLabel):
    def __init__(self, component: BaseComponent, *args, **kwargs):
        super(ComponentIcon, self).__init__(*args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        self.component = component
        self.icon = self.component.icon_qpixmap
        self.setPixmap(self.component.icon_qpixmap)
        self.info_label = QtWidgets.QLabel()
        self.info_label.setText(f"{self.component.info_value}")
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self)
        # self.create_icon()
        # self.create_info_label()

    def update(self):
        self.setPixmap(self.component.icon_qpixmap)
        self.info_label.setText(f"{self.component.info_value}")


class ConnectionPhaseDialog(QtWidgets.QDialog):
    current_id = 0
    def __init__(self, component: BaseComponent, parent=None, *args, **kwargs):
        super(ConnectionPhaseDialog, self).__init__(*args, **kwargs)
        self.component = component
        self.connection_phase = ConnectionPhase()
        self.connection_phase.compute_components()
        self.initial_layout()
        self.component_list = list(Components.components.values())
        ConnectionPhaseDialog.current_id = 0
        self.update()

    def previous_button_func(self):
        ConnectionPhaseDialog.current_id -= 1
        self.update()

    def next_button_func(self):
        ConnectionPhaseDialog.current_id += 1
        self.update()

    def reset_button_func(self):
        ConnectionPhaseDialog.current_id = 0
        self.update()

    def update(self):
        if ConnectionPhaseDialog.current_id >= len(Components.components) - 1:
            self.next_button.setEnabled(False)
        else:
            self.next_button.setEnabled(True)
        if ConnectionPhaseDialog.current_id == 0:
            self.previous_button.setEnabled(False)
        else:
            self.previous_button.setEnabled(True)
        self.current_component = self.component_list[ConnectionPhaseDialog.current_id]["instance"]
        self.current_component_label.component = self.current_component
        self.current_component_label.update()

    def initial_layout(self):
        self.setWindowTitle(f"Connection phase")
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignRight)
        # Creates an horizontal layout for the parameters
        self.current_component = Components.components[ConnectionPhaseDialog.current_id]["instance"]
        self.current_component_label = ComponentIcon(component=self.current_component, parent=self)
        self.current_component_label.setAlignment(QtCore.Qt.AlignCenter)
        self.h_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.current_component_label.layout)
        # Create buttons of the dialog
        self.previous_button = QtWidgets.QPushButton("Previous")
        self.next_button = QtWidgets.QPushButton("Next")
        self.reset_button = QtWidgets.QPushButton("Reset")
        # Add connection function
        self.previous_button.clicked.connect(self.previous_button_func)
        self.next_button.clicked.connect(self.next_button_func)
        self.reset_button.clicked.connect(self.reset_button_func)
        self.h_layout.addWidget(self.previous_button)
        self.h_layout.addWidget(self.next_button)
        self.h_layout.addWidget(self.reset_button)
        self.layout.addLayout(self.h_layout)
        self.setLayout(self.layout)
