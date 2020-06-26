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
        # self.menuBars()
        # self.setMenuBar(self.menu)
        # self.toolBars()
        # self.addToolBar(self.toolBar)

    def mainUI(self):
        self.contactTab = contactTab()
        self.favoriteTab = favoriteTab()
        self.addContactTab = addContactTab()
        self.tabs = QTabWidget()
        self.tabs.addTab(self.contactTab, "Contact")
        self.tabs.addTab(self.favoriteTab, "Favorite")
        self.tabs.addTab(self.addContactTab, "Add Contact")

    # def menuBars(self):
    #     self.menu = self.menuBar()
    #     home = self.menu.addMenu("Home")
    #     home.addAction("help")
    #     home.setToolTip("This is help")
    #     self.menu.addMenu("About")
    #     self.menu.addMenu("Price")

    # def toolPrint(self):
    #     print("Clicked!!")

    # def toolBars(self):
    #     self.toolBar = QToolBar()
    #     buttonToolbar = QAction(QIcon("img/photo-1558981285-6f0c94958bb6.jpg"), "test", self)
    #     self.toolBar.addAction(buttonToolbar)
    #     buttonToolbar.triggered.connect(self.toolPrint)

    def mainLayout(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabs)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.layout)

class contactTab(QWidget):
    def __init__(self):
        super(contactTab, self).__init__()
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

    # def addToFavorite(self):
    #     dataFavo = self.fetchFavorite
    #     print(dataFavo)

    def fetchFavorite(self, row, column):
        favoriteData = []
        favData = []
        rw = row
        cl = column
        for x in range(len(self.head)):
            res = self.table.item(int(rw),int(x)).text()
            favoriteData.append(res)
        for i in data:
            if favoriteData[0] == i['name']:
                resu = i
        return resu

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
        self.mainUI()
        self.setLayout(self.layout)

    def mainUI(self):
        self.label = QLabel("Wahyu")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)

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
        self.buttonAdd = QPushButton("Add")
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
        params = {"name": name, "number": number, "favorite": 0}
        data.append(params)
        toJson =  json.dumps(data, indent=4)
        fwrite = open('contact.json', 'w')
        fwrite.write(toJson)


if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    sys.exit(app.exec_())