import sys
from PyQt5 import QtWidgets, uic
from entrenador_electronico.plantillas.plantilla_image import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.boton_lurra.clicked.connect(self.desactivar_imagen)

    def desactivar_imagen(self):
        if self.imagen.isEnabled():
            self.imagen.setEnabled(False)
        else:
            self.imagen.setEnabled(True)



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()

    app.exec_()