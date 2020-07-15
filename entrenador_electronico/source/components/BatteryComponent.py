from entrenador_electronico.source.utils import get_content_path
from .BaseComponent import BaseComponent
from entrenador_electronico.config import config

class BatteryComponent(BaseComponent):
    counter = 0

    def __init__(self, value=config.component_dict.battery.default_value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = config.component_dict.battery.default_name
        self.icon_route = get_content_path() / "icons/battery.png"
        self.id = BatteryComponent.counter
        self.value = value
        self.unit = config.component_dict.battery.default_unit
        self.short_name = config.component_dict.battery.default_shortname
        if self.drop_event:
            BatteryComponent.counter += 1

