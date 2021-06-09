from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QLineEdit, QPushButton, \
    QLabel
from PyQt5 import QtGui
from pymongo import MongoClient
from views.main_wt import MainWT
from PyQt5.QtGui import QIcon
from settings.set import color_theme


class Autorisation(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()

        self._model = model
        self._main_controller = main_controller

        QMainWindow.__init__(self)
        self.layout = QGridLayout(self)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(self.layout)

        self.client = MongoClient()
        self.db = self.client.warehouse
        self.posts = self.db.log_pas
        self.it_w = self.db.item_warehouse
        self.db.list_collection_names(include_system_collections=False)

        #self.posts.remove({})
        if self.posts.count() == 0:
            new_posts = {
                "name": "Admin",
                "status": "Admin",
                "login": "root",
                "password": "root"
            }
            self.posts.insert_one(new_posts)

        self.setGeometry(300, 300, 300, 220)
        self.setWindowIcon(QIcon('logo.png'))
        self.title = 'АИС СКЛАД'
        self.left = 250
        self.top = 250
        self.width = 310
        self.height = 230
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        aut = """    
                QPushButton {
                   height: 50; 
               }
                QLineEdit{
                    height: 40;
                    margin-top:1;
                   margin-bottom:1;
               }
               QLabel{
                   color: red;
                   margin-left:9;
                   margin-top:0;
                   margin-bottom:0;
                   font-size: 200%;
               }
                """
        self.setStyleSheet(color_theme() + aut)

        self.log = QLineEdit()
        self.pas = QLineEdit()
        self.pas.setEchoMode(QLineEdit.Password)

        self.log.setPlaceholderText("Логин")
        self.pas.setPlaceholderText("Пароль")
        self.log.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.pas.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))

        self.auto_log = QPushButton("Войти")
        self.auto_log.clicked.connect(self.log_pass)
        self.auto_log.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))

        self.layout.addWidget(self.log, 1, 0)
        self.layout.addWidget(self.pas, 2, 0)
        self.layout.addWidget(self.auto_log, 4, 0)

    def log_pass(self):
        log = self.log.text()
        pasw = self.pas.text()
        if log != "" and pasw != "":
            for post in self.posts.find():
                if log == str(post['login']) and pasw == str(post['password']):
                    user = []
                    user.append(str(post['name']))
                    user.append(str(post['status']))
                    self.key = MainWT(self._model, self._main_controller, user=user)
                    self.key.show()
                    self.close()
                    return 0
                error = QLabel("Введен не верный логин или пароль")
                error.setWordWrap(True)
                error.setFont(QtGui.QFont('SansSerif', 12))
                self.layout.addWidget(error, 3, 0)
        else:
            error = QLabel("Введите логин и/или пароль")
            error.setFont(QtGui.QFont('SansSerif', 12))
            self.layout.addWidget(error, 3, 0)
