from pathlib import Path


def get_project_root():
    """Returns project root folder"""
    return Path(__file__).parent.parent


def get_content_path():
    return get_project_root() / "qt_gui/content"


def get_config_path():
    return get_project_root() / "config/config.yml"
