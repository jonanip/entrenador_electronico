from entrenador_electronico.source.utils import get_content_path
from .BaseComponent import BaseComponent
from entrenador_electronico.config import config
class TransistorNPNComponent(BaseComponent):
    counter = 0

    def __init__(self, value=config.component_dict.transistorNPN.default_value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = config.component_dict.transistorNPN.default_name
        self.icon_route = get_content_path() / "icons/transistorNPN.png"
        self.id = TransistorNPNComponent.counter
        self.value = value
        self.unit = config.component_dict.transistorNPN.default_unit
        self.short_name = config.component_dict.transistorNPN.default_shortname
        if self.drop_event:
            TransistorNPNComponent.counter += 1
