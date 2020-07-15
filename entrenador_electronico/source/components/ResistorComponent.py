from entrenador_electronico.source.utils import get_content_path
from .BaseComponent import BaseComponent
from config import config


class ResistorComponent(BaseComponent):
    counter = 0

    def __init__(self, value=config.component_dict.resistor.default_value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = config.component_dict.resistor.default_name
        self.icon_route = get_content_path() / "icons/resistor.png"
        self.id = ResistorComponent.counter
        self.value = value
        self.unit = config.component_dict.resistor.default_unit
        self.short_name = config.component_dict.resistor.default_shortname
        self.led_color = config.component_dict.resistor.led_color
        if self.drop_event:
            ResistorComponent.counter += 1

