from entrenador_electronico.source.components.Components import Components
from entrenador_electronico.source.components.BaseComponent import BaseComponent
from entrenador_electronico.source.components.BatteryComponent import BatteryComponent
from entrenador_electronico.source.Connections import Connections
import numpy as np

class ConnectionPhase:
    connection_board_shape = [5, 63]
    tension_board_shape = [2, 63]
    connection_board_shape_x = connection_board_shape[1]
    connection_board_shape_y = connection_board_shape[0]
    tension_board_shape_x = tension_board_shape[1]
    tension_board_shape_y = tension_board_shape[0]
    pin_distance = 2

    def __init__(self):
        self.connection_board = np.zeros(ConnectionPhase.connection_board_shape)
        self.tension_board = np.zeros(ConnectionPhase.tension_board_shape)

    def compute_components(self):
        # Compute size
        print("Computing component locations")
        self.circuit_length = self.compute_circuit_length()
        self.set_initial_pin()
        # print(self.circuit_length)
        # print(self.set_initial_pin())
        # print(Connections.connections)
        # print(Connections.connection_elements)


    @staticmethod
    def compute_circuit_length():
        circuit_length = 0
        component: BaseComponent
        for component_id in Components.components:
            print(component_id)
            component = Components.components[component_id]["instance"]
            print(component.connections_print())
            if component.__class__.__name__ == "BatteryComponent":  # Avoids batteries in the count
                continue
            circuit_length += component.element_length
            circuit_length += ConnectionPhase.pin_distance
        return circuit_length

    def set_initial_pin(self) -> int:
        self.initial_pin = round((ConnectionPhase.tension_board_shape_x - self.circuit_length) / 2.0)
        return self.initial_pin

    def find_element_connected_to_battery_plus(self, battery_component: BaseComponent):
        assert battery_component.__class__.__name__ == "BatteryComponent", "Element is not a battery"








