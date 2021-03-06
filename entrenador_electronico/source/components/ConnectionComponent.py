from entrenador_electronico.source.utils import get_content_path
from .BaseComponent import BaseComponent
from entrenador_electronico.config import config


class ConnectionComponent(BaseComponent):
    counter = 0
    # Dictionary linking connection types with icons
    icons = {"plus": get_content_path() / "icons/plus_conn.png",
             "minus": get_content_path() / "icons/minus_conn.png",
             "regular": get_content_path() / "icons/regular_conn.png",
             }
    colors = {"plus": [1, 0, 0],
             "minus": [0, 0, 1],
             "regular": [0, 1, 0]
    }

    def __init__(self, type=None, left_connection=None, right_connection=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Connection"
        self.icon_route = get_content_path() / "icons/resistor.png"
        self.id = ConnectionComponent.counter
        self.type = type
        self.left_connection = left_connection
        self.right_connection = right_connection
        self.led_color = "green"
        ConnectionComponent.counter += 1

