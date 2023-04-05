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
                self.open_new_window = MainLogged()
                self.open_new_window.show()
                self.close()
            else:
                alert("Wrong password.")
        except:
            alert("No user found.")


class MainLogged(QMainWindow):
    def __init__(self):
        super(MainLogged, self).__init__()
        loadUi('Main.ui', self)
        self.showMaximized()
        self.loginData.setText("Welcome to managment application. \nYou are logged in as: "+str(MainWindow.login))
        self.buttBrowseOrders.clicked.connect(self.BrowseOrders)
        self.buttAddClient.clicked.connect(self.AddClient)
    def BrowseOrders(self):
        self.open_new_window = BrowseOrders()
        self.open_new_window.show()
        self.close()
    def AddClient(self):
        self.open_new_window = AddClient()
        self.open_new_window.show()
        self.close()

class AddClient(QMainWindow):
    def __init__(self):
        super(AddClient, self).__init__()
        loadUi('AddClient.ui', self)
        self.BackButton.clicked.connect(self.MainLogged)
        self.ResetButton.clicked.connect(self.ResetData)
        self.AddClientButton.clicked.connect(self.AddClient)
    def MainLogged(self):
        self.open_new_window = MainLogged()
        self.open_new_window.show()
        self.close()
    def ResetData(self):
        self.CodeLine.setText("")
        self.FullNameLine.setText("")
        self.NIPLine.setText("")
        self.CityLine.setText("")
        self.EmailLine.setText("")
        self.BlockedCheckBox.setChecked(False)
    def AddClient(self):
        CODE = self.CodeLine.text()
        FULL_NAME = self.FullNameLine.text()
        NIP = self.NIPLine.text()
        CITY = self.CityLine.text()
        EMAIL = self.EmailLine.text()
        if self.BlockedCheckBox.isChecked() == True: BLOCKED = 1
        else: BLOCKED = 0

        if '@' not in EMAIL: print("ZŁY EMAIL") 
        else: print("OK EMAIL")

        cursor.execute(""" INSERT INTO APPLICATION.CLIENTS (CLIENT_CODE, CLIENT_NAME, NIP, CITY, EMAIL, BLOCKED)
                        VALUES ('%s','%s','%s','%s','%s',%s)""" % (str(CODE), str(FULL_NAME), str(NIP), str(CITY), str(EMAIL), BLOCKED))
        connection.commit()

class BrowseOrders(QMainWindow):
    def __init__(self):
        super(BrowseOrders, self).__init__()
        loadUi('BrowseOrders.ui', self)
        self.showMaximized()
        self.ordersTable.setSortingEnabled(False)
        self.ordersTable.setColumnCount(5)
        self.ordersTable.setRowCount(0)           
        self.ordersTable.setColumnWidth(0, 3000)
        self.ordersTable.setColumnWidth(1, 3000)
        self.ordersTable.setColumnWidth(2, 3000)
        self.ordersTable.setColumnWidth(3, 3000)
        self.ordersTable.setColumnWidth(4, 3000)

        

        def getOrders():
            cursor.execute("""SELECT ORDER_NAME, CLIENT, TO_CHAR(INPUT_DATE, 'dd-mm-yyyy'), TO_CHAR(REGISTRATION_DATE, 'dd-mm-yyyy'), VALUE
                            FROM ORDERS""")
            orders = cursor.fetchall()
            BrowseOrders.ORDER_NAME = [row[0] for row in orders]
            BrowseOrders.CLIENT = [row[1] for row in orders]
            BrowseOrders.INPUT_DATE = [row[2] for row in orders]
            BrowseOrders.REGISTRATION_DATE = [row[3] for row in orders]
            BrowseOrders.VALUE = [row[4] for row in orders]

            q = 0
            for i in range (0,len(BrowseOrders.ORDER_NAME)):
                self.ordersTable.setRowCount(len(BrowseOrders.ORDER_NAME))
                self.ordersTable.setItem(q, 0, QTableWidgetItem(str(BrowseOrders.ORDER_NAME[i])))
                self.ordersTable.setItem(q, 1, QTableWidgetItem(str(BrowseOrders.CLIENT[i])))
                self.ordersTable.setItem(q, 2, QTableWidgetItem(str(BrowseOrders.INPUT_DATE[i])))
                self.ordersTable.setItem(q, 3, QTableWidgetItem(str(BrowseOrders.REGISTRATION_DATE[i])))
                self.ordersTable.setItem(q, 4, QTableWidgetItem(str(BrowseOrders.VALUE[i])))
                q=q+1
            self.ordersTable.resizeRowsToContents()
            self.ordersTable.resizeColumnsToContents()
            self.ordersTable.setSortingEnabled(True)


        self.buttRefresh.clicked.connect(getOrders)
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())