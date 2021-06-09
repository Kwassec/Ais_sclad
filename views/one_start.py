from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QLineEdit, QPushButton, \
    QLabel
from PyQt5 import QtGui
from settings.set import color_theme, update_start_set


class Onestart(QMainWindow):
    def __init__(self):
        super().__init__()

        QMainWindow.__init__(self)
        self.layout = QGridLayout(self)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(self.layout)

        self.setGeometry(300, 300, 300, 220)
        self.title = 'АИС СКЛАД'
        self.left = 250
        self.top = 250
        self.width = 310
        self.height = 330
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
                          color:#a5a5a5;
                          margin-left:9;
                          margin-top:0;
                          margin-bottom:0;
                          font-size: 200%;
                      }
                       """
        self.setStyleSheet(color_theme() + aut)

        label = QLabel("Спасибо что выбрали нашу программу! Перед началом работы необходимо "
                       "указать хост подключения, логин и пароль для базы данных!")
        label.setWordWrap(True)
        label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))


        self.host = QLineEdit()
        self.host.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.log = QLineEdit()
        self.log.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.pas = QLineEdit()
        self.pas.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))

        self.host.setPlaceholderText("Host")
        self.log.setPlaceholderText("Логин")
        self.pas.setPlaceholderText("Пароль")

        self.auto_log = QPushButton("Сохранить и перезапустить")
        self.auto_log.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.auto_log.clicked.connect(self.start_set)

        self.layout.addWidget(label, 0,0)
        self.layout.addWidget(self.host, 1, 0)
        self.layout.addWidget(self.log, 2, 0)
        self.layout.addWidget(self.pas, 3, 0)
        self.layout.addWidget(self.auto_log, 4, 0)

    def start_set(self):
        self.host.text().split()
        if self.host.text()!='':
            arr = []
            arr.append(self.host.text())
            arr.append(self.log.text())
            arr.append(self.pas.text())
            update_start_set(arr)
            self.close()
