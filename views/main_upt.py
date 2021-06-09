from PyQt5.QtWidgets import QGridLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, \
    QComboBox
from pymongo import MongoClient
from PyQt5 import QtWidgets
from controllers.main_ctrl import MainController
from settings.set import color_theme


class UpdateWindow(QtWidgets.QWidget):
    def __init__(self, model, current, db):
        super().__init__()

        self.bd = db
        self.current = current
        self._model = model
        self._main_controller = MainController

        self.client = MongoClient()
        self.db = self.client.warehouse
        self.posts = self.db.item_warehouse
        self.pos_ad = self.db.log_pas
        self.db.list_collection_names(include_system_collections=False)

        self.title = 'Обновление'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 250
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet(color_theme())
        self.layout = QGridLayout(self)

        if self.bd == 1:
            self.table = QTableWidget()
            self.table.setColumnCount(4)
            self.table.setRowCount(0)
            self.table.setHorizontalHeaderLabels(["Наименование", "Поставщик","Колличество", "Склад"])
            self.table.setColumnWidth(0, 70)
            self.table.setColumnWidth(1, 180)
            self.table.setColumnWidth(4, 60)
            self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
            self.layout.addWidget(self.table, 0, 0)
            self.on_item(self.table)
        else:
            self.table = QTableWidget()
            self.table.setColumnCount(4)
            self.table.setRowCount(0)
            self.table.setHorizontalHeaderLabels(["Имя", "Статус", "Логин", "Пароль"])
            self.table.setColumnWidth(0, 70)
            self.table.setColumnWidth(1, 180)
            self.table.setColumnWidth(4, 60)
            self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
            self.layout.addWidget(self.table, 0, 0)
            self.on_item(self.table)
        self.save_btn = QPushButton("Сохранить изменения")
        self.save_btn.clicked.connect(self.save_db)
        self.layout.addWidget(self.save_btn, 1, 0)
        self.show()

    def on_item(self, table):
        self.table.setRowCount(0)
        if self.bd == 1:
            arr = self.posts.find_one()
            arr = list(arr.keys())
            db = self.posts
        else:
            arr = self.pos_ad.find_one()
            arr = list(arr.keys())
            db = self.pos_ad
        for post in db.find({arr[1]: self.current}):
            row_Position = table.rowCount()
            self.table.insertRow(row_Position)
            self.table.setItem(row_Position, 0, QTableWidgetItem(str(post[arr[1]])))
            if self.bd == 1:
                self.table.setItem(row_Position, 1, QTableWidgetItem(str(post[arr[2]])))
            else:
                self.table.setCellWidget(row_Position, 1, QComboBox())
                self.table.cellWidget(row_Position, 1).addItems(["Администратор", "Работник склад"])
            self.table.setItem(row_Position, 3, QTableWidgetItem(str(post[arr[3]])))
            self.table.setItem(row_Position, 2, QTableWidgetItem(str(post[arr[4]])))



    def save_db(self):
        if self.bd == 1:
            db = self.posts
        else:
            db = self.pos_ad
        arr = db.find_one()
        arr = list(arr.keys())
        if self.bd == 1:
            db = self.posts
            db.update({arr[1]: self.current},
                              {arr[1]: self.current,
                               arr[2]: str(self.table.model().index(0, 1).data()),
                               arr[3]: int(self.table.model().index(0, 3).data()),
                               arr[4]: int(self.table.model().index(0, 2).data())})
            self._main_controller.update_db(self, int(self.table.model().index(0, 2).data()))
            self.close()
        else:
            db = self.pos_ad
            db.update({arr[1]: self.current},
                              {arr[1]: self.current,
                               arr[2]: self.table.cellWidget(0, 1).currentText(),
                               arr[3]: str(self.table.model().index(0, 2).data()),
                               arr[4]: str(self.table.model().index(0, 3).data())})
            self._main_controller.update_db(self, 0)
            self.close()
