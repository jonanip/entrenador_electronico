import sys
from PyQt5 import QtWidgets
from entrenador_electronico.plantillas.plantilla_image import Ui_MainWindow
from PyQt5.QtGui import QIcon, QPixmap

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.boton_espacio.clicked.connect(lambda: self.cambiar_imagen(ruta="E:\AITA\pycharm\entrenador_electronico\entrenador_electronico\contenido\estacionespacial4.jpg"))
        self.boton_lurra.clicked.connect(lambda: self.cambiar_imagen(ruta="E:\AITA\pycharm\entrenador_electronico\entrenador_electronico\contenido\cuba1.jpg"))


    def desactivar_imagen(self):
        if self.imagen.isEnabled():
            self.imagen.setEnabled(False)
        else:
            self.imagen.setEnabled(True)

    def cambiar_imagen(self, ruta=None):
        q_pixmap = QPixmap(ruta)
        self.imagen.setPixmap(q_pixmap)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()

    app.exec_()