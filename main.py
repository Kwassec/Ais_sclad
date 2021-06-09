"""Project build and launch class"""
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from model.model import Model
from controllers.main_ctrl import MainController
from views.Autorisation import Autorisation
from views.one_start import Onestart
from settings.set import start_set


class App(QApplication):
    """Project build and launch class"""
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        start_set()
        self.model = Model()
        self.main_ctrl = MainController(self.model)
        if start_set() == 0:
            self.main = Onestart()
            self.main.show()
        else:
            self.main = Autorisation(self.model, self.main_ctrl)
            self.main.show()


if __name__ == '__main__':
    app = App([])
    app.setWindowIcon(QIcon('logo.png'))
    app.setStyle('Fusion')
    sys.exit(app.exec_())
