
from entrenador_electronico.source.utils import get_content_path
from .BaseComponent import BaseComponent
from entrenador_electronico.config import config
class DiodoComponent(BaseComponent):
    counter = 0

    def __init__(self, value=config.component_dict.diodo.default_value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = config.component_dict.diodo.default_name
        self.icon_route = get_content_path() / "icons/diodo.png"
        self.id = DiodoComponent.counter
        self.value = value
        self.unit = config.component_dict.diodo.default_unit
        self.short_name = config.component_dict.diodo.default_shortname
        self.led_color = config.component_dict.diodo.led_color
        if self.drop_event:
            DiodoComponent.counter += 1