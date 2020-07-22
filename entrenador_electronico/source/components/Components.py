from entrenador_electronico.source.components import BaseComponent

class Components:
    components = {}
    component_widget = {}

    @staticmethod
    def find_by_component_type(component_type: str=None):
        temp_components = []
        for component_id in Components.components:
            component_instance = Components.components[component_id]
            if component_instance.__class__.__name__ == component_type:
                temp_components.append(component_instance)
        return temp_components

    @staticmethod
    def find_components_connected_to_battery_plus(battery_component: BaseComponent):
        return battery_component.connections["left"]

    @staticmethod
    def find_components_connected_to_battery_minus(battery_component: BaseComponent):
        return battery_component.connections["right"]

    @staticmethod
    def has_connections(component: BaseComponent):
        component_connections = component.connections
        if component_connections == {"left": [], "right": []}:
            return False
        else:
            return True

