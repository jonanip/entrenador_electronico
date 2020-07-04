from PyQt5 import QtWidgets
from entrenador_electronico.templates.plantilla_image import Ui_MainWindow
from PyQt5.QtGui import QPixmap


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.boton_espacio.clicked.connect(lambda: self.cambiar_imagen(ruta="../content/estacionespacial3.jpg"))
        self.boton_lurra.clicked.connect(lambda: self.cambiar_imagen(ruta="../content/estacionespacial4.jpg"))


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