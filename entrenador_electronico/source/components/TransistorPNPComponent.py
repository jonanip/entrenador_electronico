from entrenador_electronico.source.utils import get_content_path
from .BaseComponent import BaseComponent
from entrenador_electronico.config import config
class TransistorPNPComponent(BaseComponent):
    counter = 0

    def __init__(self, value=config.component_dict.transistorPNP.default_value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = config.component_dict.transistorPNP.default_name
        self.icon_route = get_content_path() / "icons/transistorPNP.png"
        self.id = TransistorPNPComponent.counter
        self.value = value
        self.unit = config.component_dict.transistorPNP.default_unit
        self.short_name = config.component_dict.transistorPNP.default_shortname
        if self.drop_event:
            TransistorPNPComponent.counter += 1