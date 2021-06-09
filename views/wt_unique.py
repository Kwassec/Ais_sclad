from PyQt5.QtWidgets import QGridLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from pymongo import MongoClient
from PyQt5 import QtWidgets
from settings.set import color_theme


class DocWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.client = MongoClient()
        self.db = self.client.warehouse
        self.doc = self.db.documents
        self.db.list_collection_names(include_system_collections=False)

        self.title = 'Сводка о выданных предметах'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 250
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet(color_theme())
        self.layout = QGridLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(["Кем выдано","Отдел","Инвент №", "Наименование", "Поставщик", "Склад","Дата"])
        for i in range(7):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        self.layout.addWidget(self.table, 0, 0)
        self.on_item()

        self.save_btn = QPushButton("Экспорт")
        self.layout.addWidget(self.save_btn, 1, 0)


    def on_item(self):
        self.table.setRowCount(0)
        arr = self.doc.find_one()
        arr = list(arr.keys())
        row_Position = self.table.rowCount()
        for post in self.doc.find():
            self.table.insertRow(row_Position)
            self.table.setItem(row_Position, 0, QTableWidgetItem(str(post[arr[1]])))
            self.table.setItem(row_Position, 1, QTableWidgetItem(str(post[arr[2]])))
            self.table.setItem(row_Position, 2, QTableWidgetItem(str(post[arr[3]])))
            self.table.setItem(row_Position, 3, QTableWidgetItem(str(post[arr[4]])))
            self.table.setItem(row_Position, 4, QTableWidgetItem(str(post[arr[5]])))
            self.table.setItem(row_Position, 5, QTableWidgetItem(str(post[arr[6]])))
            self.table.setItem(row_Position, 6, QTableWidgetItem(str(post[arr[7]])))

