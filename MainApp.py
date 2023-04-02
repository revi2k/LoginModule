from PyQt5.uic import loadUi
import cx_Oracle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

connection = cx_Oracle.connect(user='APPLICATION', password='application1',
                               dsn="DESKTOP-GND7002/XEPDB1")
cursor = connection.cursor()

def alert(message):
    msg = QMessageBox()
    msg.setWindowTitle("Alert")
    msg.setText(message)
    x = msg.exec_()
    return x

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('Login.ui', self)
        self.loginButton.clicked.connect(self.open_window)
        self.exitButton.clicked.connect(exit)
    def exit():
        sys.exit()
    def open_window(self):
        MainWindow.login = self.loginLine.text()
        MainWindow.password = self.passwordLine.text()
        try:
            cursor.execute("SELECT LOGIN, PASSWORD FROM APPLICATION.USERS WHERE LOGIN = '%s'" % (MainWindow.login))
            LOGIN_DATA = cursor.fetchall()
            LOGIN_D = [row[0] for row in LOGIN_DATA]
            PASSWORD_D = [row[1] for row in LOGIN_DATA]

            if LOGIN_D[0] == MainWindow.login and PASSWORD_D[0] == MainWindow.password:
                self.second_window = SecondWindow()
                self.second_window.show()
                self.close()
            else:
                alert("Wrong password.")
        except:
            alert("No user found.")

class SecondWindow(QMainWindow):
    def __init__(self):
        super(SecondWindow, self).__init__()
        loadUi('Main.ui', self)
        def welcome():
            self.loginData.setText(str(MainWindow.login))
        self.clickButton.clicked.connect(welcome)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())