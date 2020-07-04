# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plantilla_imagen.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.imagen = QtWidgets.QLabel(self.centralwidget)
        self.imagen.setEnabled(True)
        self.imagen.setGeometry(QtCore.QRect(160, 20, 511, 331))
        self.imagen.setText("")
        self.imagen.setPixmap(QtGui.QPixmap("C:/Users/Txintxarri/Pictures/cuba1.jpg"))
        self.imagen.setScaledContents(True)
        self.imagen.setObjectName("imagen")
        self.boton_lurra = QtWidgets.QPushButton(self.centralwidget)
        self.boton_lurra.setEnabled(True)
        self.boton_lurra.setGeometry(QtCore.QRect(160, 410, 75, 23))
        self.boton_lurra.setObjectName("boton_lurra")
        self.boton_espacio = QtWidgets.QPushButton(self.centralwidget)
        self.boton_espacio.setGeometry(QtCore.QRect(160, 460, 75, 23))
        self.boton_espacio.setObjectName("boton_espacio")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.boton_lurra.setAccessibleDescription(_translate("MainWindow", "uuuu"))
        self.boton_lurra.setText(_translate("MainWindow", "lurra"))
        self.boton_espacio.setText(_translate("MainWindow", "espacio"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

