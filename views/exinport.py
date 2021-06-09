from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QLineEdit, QPushButton, \
    QLabel, QComboBox
from pymongo import MongoClient

from PyQt5.QtGui import QIcon
from settings.set import color_theme


class Ex_in_port(QMainWindow):
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

        self.setGeometry(300, 300, 300, 220)
        self.setWindowIcon(QIcon('web.png'))
        self.title = 'Эксопрт/Импорт'
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
                       QComboBox{height: 40;}
                        """
        self.setStyleSheet(color_theme()+aut)

        self.war_haus = QComboBox()
        self.layout.addWidget(self.war_haus, 1, 2)
        self.war_haus.setVisible(False)
        self.Table_ex_in = QComboBox(self)

        self.Ex_in = QComboBox(self)
        self.Ex_in.addItem("Экспорт")
        self.Ex_in.addItem("Импорт")
        self.ex_in_table()
        self.Ex_in.currentTextChanged.connect(lambda: self.ex_in_table())

        self.button = QPushButton("Выполнить")
        self.button.clicked.connect(lambda: self.Star_ex_in())



        self.layout.addWidget(self.Ex_in, 1, 0)
        self.layout.addWidget(self.Table_ex_in, 1, 1)
        self.layout.addWidget(self.button, 2, 0, 2,0)
        self._model.type_changed.connect(self.type_w)


    @pyqtSlot(list)
    def type_w(self, _list):
        self.war_haus.clear()
        for tp in _list:
            arr = list(tp.keys())
            self.war_haus.addItem(str(tp[arr[1]]) + " Склад")

    def ex_in_table(self):
        self.Table_ex_in.clear()
        if self.Ex_in.currentText() == "Экспорт":
            self.Table_ex_in.addItems(["Сводка о выдачи", "Предметы на складе"])
            self.war_haus.setVisible(False)
        else:
            self.Table_ex_in.addItems(["Предметы на складе"])
            self._model.type_w()
            self.war_haus.setVisible(True)


    def Star_ex_in(self):
        if self.Ex_in.currentText() == "Экспорт":
            if self.Table_ex_in.currentText() == "Сводка о выдачи":
                self._model.Export_date(1)
            else:
                self._model.Export_date(0)
        if self.Ex_in.currentText() == "Импорт":
            self._model.Import_date(self.war_haus.currentText())