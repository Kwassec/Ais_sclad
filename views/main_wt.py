# -*- codecs: utf-8 -*-
import os
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, \
    QTabWidget, QPushButton, QGroupBox, \
    QTableWidgetItem, QLabel, QComboBox, QLineEdit, QTableWidget, QAbstractItemView, \
    QHeaderView, QListWidget, QSpinBox
from views.main_upt import UpdateWindow
from views.exinport import Ex_in_port
from views.wt_unique import DocWindow
from PyQt5.QtWidgets import QMenu
import datetime
from settings.set import color_theme, update_color_theme
from settings.set import auto_input, auto_output
import jinja2


class MainWT(QMainWindow):
    def __init__(self, model, main_controller, user):
        super().__init__()

        self._model = model
        self._main_controller = main_controller
        self._user = user

        self._model.output_changed.connect(self.on_wt)
        self._model.type_changed.connect(self.type_w)

        QMainWindow.__init__(self)
        self.layout = QGridLayout(self)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(self.layout)

        self.title = 'АИС СКЛАД'
        self.left = 0
        self.top = 0
        self.width = 1100
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.aut = """    
                               QPushButton {
                                  height: 20; 
                              }
                               QLineEdit{
                                   height: 20;
                              }
                              QComboBox{height: 20;}
                               """
        self.setStyleSheet(color_theme()+self.aut)

        self._createMenuBar()

        # Вкладки
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.West)
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.unique_w()
        if self._user[1] == 'Admin':
            self.admin()

        # Статус бар
        self.status_bar = QGroupBox("Статус")
        self.layout.addWidget(self.status_bar, 1, 0)
        self.stat_layout = QGridLayout(self)
        self.status_bar.setLayout(self.stat_layout)

        self.exit = QPushButton("Выход")
        self.exit.clicked.connect(self.close)
        self.name = QLabel(self)
        if self._user[1] == 'Admin' or self._user[1] == "Администратор":
            self.name.setText(self._user[0] + ":Администратор")
        else:
            self.name.setText(self._user[0] + ":Работник")

        self.warehouse = QComboBox(self)
        self.warehouse.setCurrentIndex(0)
        self.warehouse.currentIndexChanged.connect(self.choice_type_w)

        error = QLabel("")
        error.setStyleSheet('''color: red;
                   margin-left:9;
                   margin-top:0;
                   margin-bottom:0;
                   font-size: 200%;''')
        error.setFont(QtGui.QFont('SansSerif', 12))
        self.stat_layout.addWidget(error, 0, 2,1,4)

        self.stat_layout.addWidget(self.warehouse, 0, 6)
        self.stat_layout.addWidget(self.name, 0, 0, 1, 1)
        self.stat_layout.addWidget(self.exit, 0, 7)
        self._model.type_w()

    def admin(self):
        self.tabs.addTab(self.tab2, "Админ")
        self.tab2.layout_ = QGridLayout()
        self.tab2.setLayout(self.tab2.layout_)

        self.tab_ = QTableWidget()
        self.tab_.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tab_.setColumnCount(4)
        self.tab_.setRowCount(0)
        self.tab_.setHorizontalHeaderLabels(["Имя", "Статус", "Логин", "Пароль"])
        self.tab_.setMaximumSize(1200, 1200)
        self.tab_.setMinimumSize(550, 300)
        self.tab_.setColumnWidth(0, 70)
        self.tab_.setColumnWidth(1, 180)
        self.tab_.setColumnWidth(4, 100)
        self.tab_.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        self.tab2.layout_.addWidget(self.tab_, 0, 0, 3, 1)

        # нструменты
        self.tool_box_ = QGroupBox("Инструменты")
        self.tab2.layout_.addWidget(self.tool_box_, 0, 8)
        self.vbox_ = QGridLayout()
        self.tool_box_.setLayout(self.vbox_)

        self.drop_btn_ = QPushButton("Удалить")
        self.adding_btn_ = QPushButton("Добавить")
        self.update_btn_ = QPushButton("Редактировать")

        self.adding_btn_.clicked.connect(lambda: self.adding_db(self.tab_))
        self.update_btn_.clicked.connect(lambda: self.update_db(self.tab_, 0))
        self.drop_btn_.clicked.connect(lambda: self._main_controller.
                                       user(str(self.tab_.model().
                                                index(self.tab_.currentIndex().row(), 0).data())))

        self.adding_box = QComboBox(self)
        self.adding_box.addItem("Администратор")
        self.adding_box.addItem("Работник склад")

        self.name_ = QLineEdit(self)
        self.name_.setPlaceholderText("ФИО")
        self.login_ = QLineEdit(self)
        self.login_.setPlaceholderText("Логин")
        self.password_ = QLineEdit(self)
        self.password_.setPlaceholderText("Пароль")

        self.vbox_.addWidget(self.adding_box, 0, 0)
        self.vbox_.addWidget(self.name_, 0, 1)
        self.vbox_.addWidget(self.login_, 0, 2)
        self.vbox_.addWidget(self.password_, 0, 3)
        self.vbox_.addWidget(self.adding_btn_, 0, 4)

        self.vbox_.addWidget(self.drop_btn_, 1, 1)
        self.vbox_.addWidget(self.update_btn_, 1, 2)

        # склады
        self.warehouse = QGroupBox("Складские комнаты")
        self.tab2.layout_.addWidget(self.warehouse, 1, 8, 2, 1)
        self.w_box = QGridLayout()
        self.warehouse.setLayout(self.w_box)

        self.adding_w = QComboBox(self)
        self.adding_w.addItem("Новый склад")

        self.add_w = QPushButton("Добавить")
        self.drop_w = QPushButton("Удалить")
        self.warehouse_num = QListWidget()

        self.add_w.clicked.connect(lambda: self._main_controller.update_war(self.adding_w.currentText(), 0))
        self.drop_w.clicked.connect(lambda: self._main_controller.update_war(
            self.warehouse_num.takeItem(self.warehouse_num.currentRow()).text(), 1))

        self.w_box.addWidget(self.warehouse_num, 1, 0, 1, 4)
        self.w_box.addWidget(self.adding_w, 0, 0)
        self.w_box.addWidget(self.add_w, 0, 1)
        self.w_box.addWidget(self.drop_w, 0, 3)

        self._main_controller.output_db(0, None)

    def unique_w(self):
        self.tabs.addTab(self.tab1, "Склад")
        self.tab1.layout = QGridLayout(self)

        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setColumnCount(4)
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(["Наименование", "Поставщик", "Колличество","Склад"])
        self.table.setMaximumSize(1200, 1200)
        self.table.setMinimumSize(550, 300)
        self.table.setColumnWidth(0, 180)
        self.table.setColumnWidth(1, 180)
        self.table.setColumnWidth(3, 0)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        # лайаут первой вкладки
        self.tab1.layout.addWidget(self.table, 0, 0, 3, 7)
        self.layout.addWidget(self.tabs)
        self.tab1.setLayout(self.tab1.layout)
        self.setLayout(self.layout)

        # формы поиска/ввода
        self.tool_box = QGroupBox("Инструменты")
        self.tab1.layout.addWidget(self.tool_box, 0, 8)
        self.vbox = QGridLayout()
        self.tool_box.setLayout(self.vbox)

        self.search_box = QComboBox(self)
        self.search_box.addItem("Наименование")
        self.search_box.addItem("Поставщик")
        self.search_box.addItem("Склад")

        self.search = QLineEdit(self)
        self.search.setPlaceholderText("Поиск")

        self.search_btn = QPushButton("Поиск")
        self.drop_btn = QPushButton("Удалить")
        self.adding_btn = QPushButton("Добавить")
        self.update_btn = QPushButton("Редактировать")

        self.adding_btn.clicked.connect(lambda: self.adding_db(self.table))
        self.update_btn.clicked.connect(lambda: self.update_db(self.table, 1))
        self.drop_btn.clicked.connect(lambda: self._main_controller
                                      .item(str(self.table.model()
                                                .index(self.table.currentIndex().row(), 0).data()),
                                            self.warehouse.currentText()))
        self.search_btn.clicked.connect(lambda: self.search_db(self.table))

        self.ad2 = QLineEdit(self)
        self.ad2.setPlaceholderText("Наименование")
        self.ad3 = QLineEdit(self)
        self.ad3.setPlaceholderText("Поставщик")
        self.ad4 = QLineEdit(self)
        self.ad4.setPlaceholderText("Колличесвто")

        self.vbox.addWidget(self.search_box, 0, 0)
        self.vbox.addWidget(self.search, 0, 1, 1, 2)
        self.vbox.addWidget(self.search_btn, 0, 3)

        self.vbox.addWidget(self.adding_btn, 1, 3)
        self.vbox.addWidget(self.ad2, 1, 0)
        self.vbox.addWidget(self.ad3, 1, 1)
        self.vbox.addWidget(self.ad4, 1, 2)

        self.vbox.addWidget(self.drop_btn, 2, 1)
        self.vbox.addWidget(self.update_btn, 2, 2)

        ############## заявки ###########################
        self.log_box = QGroupBox("Заявки")
        self.tab1.layout.addWidget(self.log_box, 1, 8, 2, 1)
        self.vbox_ = QGridLayout()
        self.log_box.setLayout(self.vbox_)

        self.department = QLineEdit()
        self.department.setPlaceholderText("Отдел")
        self.add_num = QPushButton("Добавить")
        self.dep_btn = QPushButton("Оформить")
        self.ded_btn = QPushButton("Очистить")

        ####################################################
        self.in_num = QTableWidget()
        self.in_num.setColumnCount(3)
        self.in_num.setRowCount(0)
        self.in_num.setHorizontalHeaderLabels(["Наименование", "Склад", "Колличество"])
        self.in_num.setColumnWidth(1, 100)
        self.in_num.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.in_num.setMaximumSize(400, 300)
        ######################################################

        self.add_num.clicked.connect(self.add_list)
        self.ded_btn.clicked.connect(self.ded_list)
        self.dep_btn.clicked.connect(self.create_docx)

        self.vbox_.addWidget(self.department, 0, 0, 1, 2)
        self.vbox_.addWidget(self.in_num, 1, 0, 4, 1)
        self.vbox_.addWidget(self.dep_btn, 1, 1)
        self.vbox_.addWidget(self.add_num, 2, 1)
        self.vbox_.addWidget(self.ded_btn, 3, 1)

        self._main_controller.output_db(1, None)

    @pyqtSlot(list)
    def on_wt(self, _dict):
        if _dict[0] == 0:
            table = self.tab_
        else:
            table = self.table
        _dict.pop(0)
        table.setRowCount(0)
        row = table.rowCount()
        for post in _dict:
            arr = list(post.keys())
            if str(post[arr[1]]) != "":
                table.insertRow(row)
                table.setItem(row, 0, QTableWidgetItem(str(post[arr[1]])))
                table.setItem(row, 1, QTableWidgetItem(str(post[arr[2]])))
                table.setItem(row, 2, QTableWidgetItem(str(post[arr[4]])))
                if table == self.table:
                    if int(table.item(row, 2).text()) <= 20:
                        table.item(row, 2).setBackground(QColor(139,0,0))
                    elif int(table.item(row, 2).text()) <= 60:
                        table.item(row, 2).setBackground(QColor(213,62,7))
                table.setItem(row, 3, QTableWidgetItem(str(post[arr[3]])))
        return 0

    @pyqtSlot(list)
    def type_w(self, _list):
        self.warehouse.clear()
        if self._user[1] == 'Admin' or self._user[1] == "Администратор":
            self.warehouse_num.clear()
        for tp in _list:
            arr = list(tp.keys())
            self.warehouse.addItem(str(tp[arr[1]]) + " Склад")
            if self._user[1] == 'Admin' or self._user[1] == "Администратор":
                if int(tp[arr[1]]) == 1:
                    self.warehouse_num.addItem("Склад : "+str(tp[arr[1]])+" - 2 Предмета на складе")
                else:
                    self.warehouse_num.addItem("Склад : " + str(tp[arr[1]]) + " - 0 Предмета на складе")

    def choice_type_w(self, i):
        arr = self.warehouse.currentText()
        arr = list(arr.split())
        if len(arr) == 0:
            self._main_controller.output_db(1, None)
        else:
            self._main_controller.output_db(int(arr[0]), None)

    def _createMenuBar(self):
        self.menuBar = self.menuBar()
        self.fileMenu = QMenu("File", self)
        self.fileMenu.addAction("Import/Export", lambda : self.ex_in())
        self.fileMenu.addAction("Сводка", lambda: self.doc_un())
        self.fileMenu.addAction("Exit", lambda: self.close())
        self.menuBar.addMenu(self.fileMenu)
        self.setMenu = self.menuBar.addMenu("Settings")
        self.findMenu = self.setMenu.addMenu("Color Theme")
        self.findMenu.addAction("Dark", lambda: self.theme_update("dark"))
        self.findMenu.addAction("light", lambda: self.theme_update("light"))
        self.helpMenu = self.menuBar.addMenu("Help").Action(lambda: self.help())
        self.helpMenu.addAction("help function", lambda: self.help())


    def ex_in(self):
        self.key = Ex_in_port(model= self._model, main_controller=self._main_controller)
        self.key.show()

    def theme_update(self, value):
        update_color_theme(value)
        self.setStyleSheet(color_theme()+self.aut)

    def update_db(self, table, db):
        if table.currentIndex().row() == -1:
            return 0
        self.key = UpdateWindow(self._model,
                                current=format(table.model().index(table.currentIndex().row(), 0).data()),
                                db=db)
        self.key.show()

    def adding_db(self, table):
        arr_ = []
        if table == self.table:
            arr = self.warehouse.currentText()
            arr = list(arr.split())
            arr_.append(self.ad2.text().strip())
            arr_.append(self.ad3.text().strip())
            arr_.append(self.ad4.text().strip())
            arr_.append(int(arr[0]))
            self.ad2.setText("")
            self.ad3.setText("")
            self.ad4.setText("")
            self._main_controller.adding_list(arr_)
        else:
            arr_.append(self.name_.text().strip())
            arr_.append(self.adding_box.currentText().strip())
            arr_.append(self.login_.text().strip())
            arr_.append(self.password_.text().strip())
            self.name_.setText("")
            self.login_.setText("")
            self.password_.setText("")
            self._main_controller.adding_list(arr_)

    def search_db(self, table):
        if table == self.table:
            number = self.warehouse.currentIndex() + 1
            value = self.search.text()
            key = self.search_box.currentText()
            self.search.setText("")
            if key == "Наименование":
                key = "name"
            if key == "Поставщик":
                key = "provider"
            if key == "Склад":
                key = "warehouse"
            if value == '':
                self._main_controller.output_db(number, None)
        value = value.strip()
        value = "\w*" + value + "\w*"
        self._main_controller.output_db(number, {key: {'$regex': value, "$options": 'i'}})

    def create_docx(self):
        if self.department.text() != "":
            date = datetime.datetime.now()
            update = []
            update.append(self.name.text())
            for lain in range(self.in_num.rowCount()):
                update.append(self.in_num.item(lain, 0).text() +
                               " : " + str(self.in_num.cellWidget(lain, 2).value()) +
                               " : " + self.in_num.item(lain, 1).text())
            update_tu = update
            name = update_tu[0]
            update_tu.pop(0)
            get_dep = []
            for i in range(len(update_tu)):
                item = []
                item.append(list(update_tu[i].replace(':', '').split()))
                number = item[0]
                for j in range(int(number[2])):
                    ai = auto_input()
                    ai = int(ai)
                    ai += 1
                    it = []
                    it.append(ai)
                    it.append(number[0])
                    it.append(number[1])
                    it.append("Выдано с "+number[3]+" склада")
                    get_dep.append(it)
                    auto_output(ai)
            print(get_dep)
            table = ""
            for i in range(len(get_dep)):
                item = get_dep[i]
                table = table + "<tr><td>" + str(item[0]) \
                        + "</td><td>" + item[1] + "</td><td>" \
                        + item[2] + "</td><td>" + item[3] + "</td></tr>"
            template = jinja2.Template("""\
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <title>monitor_page</title>
            </head>
            <body>
            <style>
                .table {border: 1px solid black;}
                .table th {border: 1px solid black;}
                .table td {border: 1px solid black;}
                .table{border-collapse: collapse;}
            </style>
            <p>Выдать: {{dep}}-отдел</p>
            <table class="table">
            <tr>
                <th> Инвентарный № </th>
                <th> Наименование </th>
                <th> Поставщик </th>
                <th>Выдано</th>
            </tr>
            {{table}}
            </table>
            <p>_______________________________________________________________________________</p>
            <p>Подпись начальника отдела/________________/Расшифровка/_______________</p>
            <p>Подпись начальника склада/________________/Расшифровка/_______________</p>
            <p>Дата:{{date}}</p>
            <script type="text/javascript">
            window.onload = function() { window.print(); }
            </script>
            </body>
            </html> """)
            html = template.render(table=table, dep=self.department.text(),
                                   date=date.strftime("%d-%m-%Y"))
            with open('template.html', 'w') as f:
                f.write(html)
            os.system("start template.html")
            self._model.adding_department(get_dep, self.department.text(), name)

    def add_list(self):
        name = format(self.table.model()
                         .index(self.table.currentIndex().row(), 0).data())
        provider = format(self.table.model()
                         .index(self.table.currentIndex().row(), 1).data())
        w_haus = format(self.table.model()
                         .index(self.table.currentIndex().row(), 3).data())
        max_size = format(self.table.model()
                         .index(self.table.currentIndex().row(), 2).data())
        row = self.in_num.rowCount()
        self.in_num.insertRow(row)
        self.in_num.setItem(row, 0, QTableWidgetItem(name+" : "+provider))
        self.in_num.setItem(row, 1, QTableWidgetItem(w_haus))
        self.in_num.setCellWidget(row, 2, QSpinBox())
        self.in_num.cellWidget(row, 2).setMinimum(1)
        self.in_num.cellWidget(row, 2).setMaximum(int(max_size))

    def ded_list(self):
        row = self.in_num.currentIndex().row()
        self.in_num.removeRow(row)

    def doc_un(self):
        self.key = DocWindow()
        self.key.show()

    def help(self):
        os.system("start help.pdf")
