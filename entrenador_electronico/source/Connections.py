from typing import List

from PyQt5 import QtCore

class Connections:
    """Stores the connections present in the model"""
    counter = 0
    connecting = False
    connections = []
    connection_elements = []
    board_connections = []
    has_connections = False
    connection_board = None
    tension_board = None
    component_board = None

    @staticmethod
    def get_connection_lines(connection, frame) -> List:
        element_1 = Connections.connection_elements[connection[0]]
        element_2 = Connections.connection_elements[connection[1]]
        # print(f"{element_1.mapFrom(self, element_1.pos()).x()} {element_1.mapFrom(self, element_1.pos()).y()} {element_2.mapFrom(self, element_1.pos()).x()} {element_1.mapFrom(self, element_2.pos()).y()}")
        element_1_global = element_1.mapToGlobal(element_1.rect().center())
        element_2_global = element_2.mapToGlobal(element_2.rect().center())
        # print(f"Local: {self.mapFromGlobal(element_1.mapToGlobal())}")
        # Line 1
        x_1 = frame.mapFromGlobal(element_1_global).x()
        y_1 = frame.mapFromGlobal(element_1_global).y()
        x_2 = frame.mapFromGlobal(element_2_global).x()
        y_2 = frame.mapFromGlobal(element_2_global).y()

        if element_1.side == "right" and element_2.side == "left":
            if x_2 > x_1:
                q_2 = QtCore.QPoint(x_2, y_1)
            elif x_2 <= x_1:
                q_2 = QtCore.QPoint(x_2, y_1)
        if element_1.side == "right" and element_2.side == "right":
            if x_2 > x_1:
                q_2 = QtCore.QPoint(x_2, y_1)
            elif x_2 <= x_1:
                q_2 = QtCore.QPoint(x_1, y_2)

        if element_1.side == "left" and element_2.side == "left":
            if x_2 > x_1:
                q_2 = QtCore.QPoint(x_1, y_2)
            elif x_2 <= x_1:
                q_2 = QtCore.QPoint(x_2, y_1)

        if element_1.side == "left" and element_2.side == "right":
            if x_2 > x_1:
                q_2 = QtCore.QPoint(x_1, y_2)
            elif x_2 <= x_1:
                q_2 = QtCore.QPoint(x_1, y_2)

        q_1 = QtCore.QPoint(x_1, y_1)
        q_3 = q_2
        q_4 = QtCore.QPoint(x_2, y_2)
        lines = [[q_1, q_2], [q_3, q_4]]
        return lines