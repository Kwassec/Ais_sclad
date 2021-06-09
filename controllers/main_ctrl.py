from PyQt5.QtCore import QObject, pyqtSlot


class MainController(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model

    @pyqtSlot(str)
    def item(self, item, tp_w):
        self._model.delete_item(item, tp_w)

    @pyqtSlot(list)
    def output_db(self, table, param):
        arr = []
        arr.append(table)
        arr.append(param)
        self._model.output(arr)

    @pyqtSlot(str)
    def user(self, value):
        self._model.delete_user(value)

    @pyqtSlot(list)
    def adding_list(self, value):
        for i in value:
            if i == "":
                return 0
        if value[1] == "Администратор" or value[1] == "Работник склад":
            self._model.adding_user(value)
        else:
            self._model.adding_item(value)


    @pyqtSlot(int)
    def update_db(self, value):
        self._model.update_db(value)

    def update_war(self, value, index):
        if index == 1:
            arr = list(value.split())
            self._model.drop_war(str(arr[2]))
        else:
            self._model.adding_war(value)
