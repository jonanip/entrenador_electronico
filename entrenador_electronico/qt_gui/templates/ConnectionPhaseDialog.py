from PyQt5 import QtGui, QtWidgets, QtCore
from entrenador_electronico.config import config
from entrenador_electronico.source.components import BaseComponent, ConnectionComponent
from entrenador_electronico.source.components.Components import Components
from entrenador_electronico.source.ConnectionPhase import ConnectionPhase
from entrenador_electronico.source.Connections import Connections
from entrenador_electronico.source.LedMapper import LedMapper
import threading
import time

class ComponentIcon(QtWidgets.QLabel):
    def __init__(self, component: BaseComponent, *args, **kwargs):
        super(ComponentIcon, self).__init__(*args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        self.component = component
        self.icon = self.component.icon_qpixmap
        self.setPixmap(self.component.icon_qpixmap)
        self.info_label = QtWidgets.QLabel()
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self)

    def update(self):
        if self.component.__class__.__name__ != "ConnectionComponent":
            self.setPixmap(self.component.icon_qpixmap)
            self.info_label.setText(
                f"{self.component.name} {self.component.id} | <-- {self.component.get_pins[0]} | {self.component.global_id} | {self.component.get_pins[1]} --> ")
        else:
            self.component.icon_route = ConnectionComponent.icons[self.component.type]
            self.setPixmap(self.component.icon_qpixmap)
            self.info_label.setText(
                f"{self.component.name} {self.component.id} | <-- {self.component.left_connection['board']} {self.component.left_connection['pos']} | {self.component.counter} | {self.component.right_connection['board']} {self.component.right_connection['pos']} --> ")


class ConnectionPhaseDialog(QtWidgets.QDialog):
    current_id = 0

    def __init__(self, parent=None, led_mapper=None, *args, **kwargs):
        super(ConnectionPhaseDialog, self).__init__(*args, **kwargs)
        self.threads = []
        if led_mapper:
            self.led_mapper = led_mapper
        self.connection_phase = ConnectionPhase()
        self.connection_phase.compute_components()
        self.connection_phase.set_board_matrixes()
        self.component_list = list(Components.components.values())
        self.component_list = list(filter(None.__ne__, [None if component.__class__.__name__ == "BatteryComponent" else component for component in self.component_list]))
        self.component_list = list(filter(lambda component: component.connection_loop, self.component_list))
        ConnectionComponent.counter = 0
        for connection in Connections.board_connections:
            self.component_list.append(ConnectionComponent(type=connection["type"],
                                                           left_connection=connection["left"],
                                                           right_connection=connection["right"],
                                                           ))
        # self.led_mapper.lights_in_order()
        ConnectionPhaseDialog.current_id = 0
        self.initial_layout()
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
        self.current_component = self.component_list[ConnectionPhaseDialog.current_id]
        if self.current_component.__class__.__name__ == "ConnectionComponent":
            LedMapper.connection_phase = True
            LedMapper.component_phase = False
        else:
            LedMapper.connection_phase = False
            LedMapper.component_phase = True
        self.current_component_label.component = self.current_component
        self.current_component_label.update()
        if ConnectionPhaseDialog.current_id >= len(self.component_list) - 1:
            self.next_button.setEnabled(False)
        else:
            self.next_button.setEnabled(True)
        if ConnectionPhaseDialog.current_id == 0:
            self.previous_button.setEnabled(False)
        else:
            self.previous_button.setEnabled(True)
        if config.general.led_system:
            self.update_lights()

    def update_lights(self):
        LedMapper.counter += 1
        for thread in self.threads:
            thread.join()
        thread = threading.Thread(target=self.led_mapper.update_main_board_lights, args=(self.current_component, self.component_list), daemon=True)
        self.threads.append(thread)
        thread.start()

    def update_lights_local(self):
        LedMapper.counter += 1
        for thread in self.threads:
            thread.join()
        thread = threading.Thread(target=LedMapper.update_main_board_lights, args=(self.current_component, self.component_list), daemon=True)
        self.threads.append(thread)
        thread.start()


    def initial_layout(self):
        self.setWindowTitle(f"Connection phase")
        self.layout = QtWidgets.QVBoxLayout()
        # Creates an horizontal layout for the parameters
        self.current_component: BaseComponent = self.component_list[ConnectionPhaseDialog.current_id]
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

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if config.general.led_system:
            self.led_mapper.lights_off()
            LedMapper.counter += 1