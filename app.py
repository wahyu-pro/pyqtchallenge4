from PyQt5.QtWidgets import *
import sys, json
from PyQt5.QtGui import QIcon

with open('contact.json', 'r') as contact:
    data = json.load(contact)

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.mainUI()
        self.mainLayout()
        self.setCentralWidget(self.mainWidget)
        self.menuBars()
        self.setMenuBar(self.menu)
        self.toolBars()
        self.addToolBar(self.toolBar)
        self.setWindowTitle("Phone Book")
        self.setWindowIcon(QIcon("icon/bookphone.png"))

    def mainUI(self):
        self.contactTab = contactTab()
        self.favoriteTab = favoriteTab()
        self.addContactTab = addContactTab()
        self.tabs = QTabWidget()
        self.tabs.addTab(self.contactTab, QIcon("icon/contact.png"), "Contact")
        self.tabs.addTab(self.favoriteTab, QIcon("icon/favorite.png"), "Favorite")
        self.tabs.addTab(self.addContactTab, QIcon("icon/addContact.png"), "Add Contact")

    def menuBars(self):
        self.menu = self.menuBar()
        file = self.menu.addMenu("File")
        app = self.menu.addMenu("App")
        app.addAction("About")
        app.triggered.connect(self.toolPrint)

    def toolPrint(self):
        QMessageBox.information(self, "About", "This is app phone book")

    def toolBars(self):
        self.toolBar = QToolBar()
        buttonToolbar = QAction(QIcon("icon/tandatanya2.png"), "test", self)
        self.toolBar.addAction(buttonToolbar)
        buttonToolbar.triggered.connect(self.toolPrint)

    def mainLayout(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabs)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.layout)

class contactTab(QWidget):
    def __init__(self):
        super(contactTab, self).__init__()
        self.dataFavorite = {}
        self.createTable()
        self.mainUI()
        self.setLayout(self.layout)

    def mainUI(self):
        self.btnAddFavorite = QPushButton("Add to favorite")
        self.btnAddFavorite.clicked.connect(self.addToFavorite)
        # set widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.btnAddFavorite)

    def addToFavorite(self):
        if self.dataFavorite == {}:
            QMessageBox.warning(self, "Warning", "Please select contact")
        else:
            for i in data:
                if self.dataFavorite['name'] == i['name']:
                    i['favorite'] = 1
            toJson =  json.dumps(data, indent=4)
            fwrite = open('contact.json', 'w')
            fwrite.write(toJson)
            QMessageBox.information(self, "About", "Contact successfully added to favorite")
            favoriteTab.createTable

    def fetchFavorite(self, row, column):
        favoriteData = []
        rw = row
        cl = column
        for x in range(len(self.head)):
            res = self.table.item(int(rw),int(x)).text()
            favoriteData.append(res)
        for i in data:
            if favoriteData[0] == i['name']:
                self.dataFavorite.update(i)

    def createTable(self):
        self.head = ["name", "number"]
        row = len(list(data))
        self.table = QTableWidget()
        self.table.setRowCount(row)
        self.table.setColumnCount(len(self.head))
        for row in range(len(data)):
            for col in range(len(self.head)):
                if col == 0:
                    self.table.setItem(row,col,QTableWidgetItem(data[row]["name"]))
                elif col == 1:
                    self.table.setItem(row,col,QTableWidgetItem(data[row]["number"]))

        self.table.setHorizontalHeaderLabels(self.head)

        self.table.cellClicked.connect(self.fetchFavorite)

class favoriteTab(QWidget):
    def __init__(self):
        super(favoriteTab, self).__init__()
        self.dataFavorite = {}
        self.createTable()
        self.mainUI()
        self.setLayout(self.layout)

    def mainUI(self):
        self.btnDeleteFavorite = QPushButton("Delete from favorite")
        self.btnDeleteFavorite.clicked.connect(self.deleteFromfavorite)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.btnDeleteFavorite)

    def createTable(self):
        self.head = ["name", "number"]
        self.contactFav = list(filter(lambda a: a["favorite"] == 1, data))
        row = len(self.contactFav)
        self.table = QTableWidget()
        self.table.setRowCount(row)
        self.table.setColumnCount(len(self.head))
        for row in range(len(self.contactFav)):
            for col in range(len(self.head)):
                if col == 0:
                    self.table.setItem(row,col,QTableWidgetItem(self.contactFav[row]["name"]))
                elif col == 1:
                    self.table.setItem(row,col,QTableWidgetItem(self.contactFav[row]["number"]))

        self.table.setHorizontalHeaderLabels(self.head)
        self.table.cellClicked.connect(self.fetchFavorite)

    def fetchFavorite(self, row, column):
        favoriteData = []
        rw = row
        cl = column
        for x in range(len(self.head)):
            res = self.table.item(int(rw),int(x)).text()
            favoriteData.append(res)
        for i in data:
            if favoriteData[0] == i['name']:
                self.dataFavorite.update(i)

    def deleteFromfavorite(self):
        if self.dataFavorite == {}:
            QMessageBox.warning(self, "Warning", "Please select contact")
        else:
            for i in data:
                if self.dataFavorite['name'] == i['name']:
                    i['favorite'] = 0
            toJson =  json.dumps(data, indent=4)
            fwrite = open('contact.json', 'w')
            fwrite.write(toJson)
            QMessageBox.information(self, "About", "Contact successfully remove from favorite")
            self.createTable



class addContactTab(QWidget):
    def __init__(self):
        super(addContactTab, self).__init__()
        self.mainUI()
        self.setLayout(self.layout)

    def mainUI(self):
        self.inputName = QLineEdit()
        self.inputName.setPlaceholderText("Add name here ...")
        self.inputNumber = QLineEdit()
        self.inputNumber.setPlaceholderText("Add number here ...")
        # push button
        self.buttonAdd = QPushButton("Add to Contact")
        # signal slot push button
        self.buttonAdd.clicked.connect(self.add)
        # signal slot line edit
        self.inputNumber.returnPressed.connect(self.add)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.inputName)
        self.layout.addWidget(self.inputNumber)
        self.layout.addWidget(self.buttonAdd)

    def add(self):
        name = self.inputName.text()
        number = self.inputNumber.text()
        if name == "" and number == "":
            QMessageBox.warning(self, "Warning", "Please input name and number !")
        else:
            params = {"name": name, "number": number, "favorite": 0}
            data.append(params)
            toJson =  json.dumps(data, indent=4)
            fwrite = open('contact.json', 'w')
            fwrite.write(toJson)
            QMessageBox.information(self, "About", "Contact successfully added")


if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    sys.exit(app.exec_())