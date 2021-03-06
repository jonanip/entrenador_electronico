from setuptools import setup
import pathlib
import os

with open("./requirements.txt") as requirements_file:
    req = requirements_file.read()

icon_files = pathlib.Path("entrenador_electronico/qt_gui/content/icons").glob("*.png")
icon_files = [os.path.relpath(p) for p in icon_files]

setup(
    name='entrenador_electronico',
    version='0.3',
    packages=['entrenador_electronico.config', 'entrenador_electronico', 'entrenador_electronico.tests', 'entrenador_electronico.qt_gui',
              'entrenador_electronico.qt_gui.templates', 'entrenador_electronico.source',
              'entrenador_electronico.source.components'],
    url='',
    license='',
    author='Txintxarri',
    author_email='aitirga@gmail.com',
    data_files=[('config', ['entrenador_electronico/config/config.yml', 'entrenador_electronico/config/conda_env_config.yml']),
                ('icons', icon_files)
                ],
    include_package_data=True,
    description='',
    install_requires=req,
)
