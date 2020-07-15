from PyQt5 import QtGui

from entrenador_electronico.source.utils import get_content_path
from entrenador_electronico.source.components.Components import Components
from entrenador_electronico.source.Connections import Connections
from typing import List

import numpy as np

class BaseComponent(object):
    counter = 0

    def __init__(self, value=None, drop_event=None, left_connection=None, right_connection=None, *args, **kwargs):
        self.name = "default_name"
        self.drop_event = drop_event
        self.icon_route = get_content_path()
        self.value = value
        self.unit = "ohm"
        self.short_name = "R"
        self.id = BaseComponent.counter
        self.global_id = BaseComponent.counter
        self.element_length = 3
        self.left_connection_id = None
        self.right_connection_id = None
        if self.drop_event:
            BaseComponent.counter += 1
        Components.components[self.global_id] = self
        self.left_pin = [None, None]
        self.right_pin = [None, None]
        self.connection_loop = False
        self.type = None
        self.left_connection = left_connection
        self.right_connection = right_connection
        self.led_color = "red"
        self.board = None

    @property
    def icon_path(self):
        return str(self.icon_route)

    @property
    def icon_qicon(self):
        return QtGui.QIcon(self.icon_path)

    @property
    def icon_qpixmap(self):
        return QtGui.QPixmap(self.icon_path)

    @property
    def info_value(self):
        if self.value:
            return f"{self.value} {self.unit}"
        else:
            return ""

    @property
    def status_value(self):
        if self.value:
            return f"{self.name} {self.__class__.counter} -> {self.info_value}"
        else:
            return f"{self.name} {self.__class__.counter}"

    @property
    def component_value(self):
        if self.value:
            return float(self.value)
        else:
            return 0.0

    def delete_component(self):
        Components.components.pop(self.global_id)

    @property
    def has_connections(self):
        component_connections = self.connections
        if component_connections == {"left": [], "right": []}:
            return False
        else:
            return True

    @property
    def left_vertex(self):
        return Connections.connection_elements[self.left_connection_id]

    @property
    def right_vertex(self):
        return Connections.connection_elements[self.right_connection_id]

    @property
    def connections(self):
        """Computes the connections of the element"""
        component_connections = {"left": [], "right": []}
        connection: List
        for connection in Connections.connections:
            if self.left_connection_id in connection:
                temp_connection = list(connection)
                temp_connection.remove(self.left_connection_id)
                connected_vertex = Connections.connection_elements[temp_connection[0]]
                connected_parent = connected_vertex.parent_element
                component_connections["left"].append({"component": connected_parent, "connection": connected_vertex})

            if self.right_connection_id in connection:
                temp_connection = list(connection)
                temp_connection.remove(self.right_connection_id)
                connected_vertex = Connections.connection_elements[temp_connection[0]]
                connected_parent = connected_vertex.parent_element
                component_connections["right"].append({"component": connected_parent, "connection": connected_vertex})
        return component_connections

    @property
    def get_pins(self):
        pins = np.argwhere(Connections.component_board[:] == self.global_id)
        # assert len(pins) == self.element_length
        print(pins)
        return [pins[0], pins[-1]]

    def connections_print(self):
        print("--- Connection info ---")
        print(f"{self.name} {self.id} is connected with:")
        connections = self.connections
        print("Left:")
        for element in connections["left"]:
            print(f"\t{element[0].name} {element[0].id} -> {element[1].side}")
        print("Right:")
        for element in connections["right"]:
            print(f"\t{element[0].name} {element[0].id} -> {element[1].side}")
        print("--- End Connection info ---")

    def print_pins(self):
        connection_pins = 0