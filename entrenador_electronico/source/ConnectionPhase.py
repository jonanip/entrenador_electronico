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
    regular_connection_counter = 0

    def __init__(self):
        self.connection_board = -np.ones(ConnectionPhase.connection_board_shape)
        self.component_board = -np.ones(ConnectionPhase.connection_board_shape)
        self.tension_board = -np.ones(ConnectionPhase.tension_board_shape)
        self.is_batteries = False
        self.current_component_r = 0
        self.current_component_c = 0
        self.current_tension_r = 0
        self.current_tension_c = 0

    def compute_components(self):
        # Compute size
        print("Computing component locations")
        self.circuit_length = self.compute_circuit_length()
        self.set_initial_pin()
        # Check if batteries exist
        batteries = Components.find_by_component_type(component_type="BatteryComponent")
        if batteries:
            battery_0: BaseComponent = batteries[0]
            if battery_0.has_connections:
                first_component: BaseComponent = Components.find_components_connected_to_battery_plus(battery_0)[0]["component"]
                first_component_connection = Components.find_components_connected_to_battery_plus(battery_0)[0]["connection"]
                self.component_board[self.current_component_r, self.initial_pin:self.initial_pin + first_component.element_length] = first_component.global_id
                first_component.left_pin = [self.current_component_r, self.initial_pin]
                first_component.right_pin = [self.current_component_r, self.initial_pin + first_component.element_length]
                self.tension_board[0, self.initial_pin] = 1
                self.connection_board[self.current_component_r + 1, self.initial_pin] = 1
                self.current_component_c = self.initial_pin + first_component.element_length + ConnectionPhase.pin_distance
                first_component.connection_loop = True
                Connections.board_connections.append({"type": "plus",
                                                      "left": {"board": "tension board", "pos": [0, self.initial_pin]},
                                                      "right": {"board": "main board", "pos": [self.current_component_r + 1, self.initial_pin]}
                                                      })
                # Set-up connections

        # Set-up the other connected elements
                connection_loop = True
                current_component = first_component
                current_component_connection = first_component_connection
                while connection_loop:
                    next_current_component_connection = first_component.left_vertex if current_component_connection.side == "right" else first_component.right_vertex
                    next_component: BaseComponent = current_component.connections[next_current_component_connection.side][0]["component"]
                    next_component_connection = current_component.connections[next_current_component_connection.side][0]["connection"]
                    if next_component_connection.parent_element == battery_0:
                        connection_loop = False
                    self.component_board[self.current_component_r, self.current_component_c: self.current_component_c + next_component.element_length] = next_component.global_id
                    # Set-up connection
                    if next_component_connection.parent_element == battery_0:
                        self.connection_board[
                            self.current_component_r + 1, self.current_component_c - ConnectionPhase.pin_distance - 1] = 2
                        self.tension_board[1, self.current_component_c - ConnectionPhase.pin_distance] = 2
                        Connections.board_connections.append({"type": "minus",
                                                              "left": {"board": "tension board",
                                                                       "pos": [1, self.current_component_c - ConnectionPhase.pin_distance]},
                                                              "right": {"board": "main board",
                                                                        "pos": [self.current_component_r + 1,
                                                                                self.current_component_c - ConnectionPhase.pin_distance - 1]}
                                                              })

                    else:
                        self.connection_board[self.current_component_r + 1, self.current_component_c - ConnectionPhase.pin_distance - 1] = ConnectionPhase.regular_connection_counter + 10
                        self.connection_board[
                            self.current_component_r + 1, self.current_component_c] = ConnectionPhase.regular_connection_counter + 10

                        Connections.board_connections.append({"type": "regular",
                                                              "left": {"board": "main board",
                                                                       "pos": [self.current_component_r + 1, self.current_component_c - ConnectionPhase.pin_distance - 1]},
                                                              "right": {"board": "main board",
                                                                        "pos": [self.current_component_r + 1,
                                                                                self.current_component_r + 1, self.current_component_c]}
                                                              })
                    ConnectionPhase.regular_connection_counter += 1

                    self.current_component_c = self.current_component_c + next_component.element_length + ConnectionPhase.pin_distance
                    next_component.connection_loop = True
                    current_component = next_component
                    current_component_connection = next_component_connection
        self.set_board_matrixes()


    @staticmethod
    def compute_circuit_length():
        circuit_length = 0
        component: BaseComponent
        for component_id in Components.components:
            component = Components.components[component_id]
            if not component.has_connections:
                continue
            if component.__class__.__name__ == "BatteryComponent":  # Avoids batteries in the count
                continue
            circuit_length += component.element_length
            circuit_length += ConnectionPhase.pin_distance
        return circuit_length

    def set_initial_pin(self) -> int:
        self.initial_pin = round((ConnectionPhase.tension_board_shape_x - self.circuit_length) / 2.0)
        return self.initial_pin

    def set_board_matrixes(self):
        Connections.component_board = self.component_board
        Connections.tension_board = self.tension_board
        Connections.connection_board = self.connection_board










