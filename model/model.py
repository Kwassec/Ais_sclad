import os

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from pymongo import MongoClient
import datetime
from settings.set import auto_input, auto_output
import pandas as pd
from collections import OrderedDict


class Model(QObject):
    update_changed = pyqtSignal()
    output_changed = pyqtSignal(list)
    type_changed = pyqtSignal(list)
    item_changed = pyqtSignal(str)
    adding_changed = pyqtSignal(list)

    @property
    def users(self):
        return self._item

    @property
    def item(self):
        return self._item

    @property
    def list_arr(self):
        return self._list

    # user
    def delete_user(self, _item):
        arr = self.pos_ad.find_one()
        arr = list(arr.keys())
        self.pos_ad.remove({arr[1]: _item})
        arr = [0, None]
        self.output(arr)

    def adding_user(self, _list):
        arr = list(self.pos_ad.find_one().keys())
        new_posts = {
            arr[1]: _list[0],
            arr[2]: _list[1],
            arr[3]: _list[2],
            arr[4]: _list[3]
        }
        self.pos_ad.insert_one(new_posts)
        arr = [0, None]
        self.output(arr)

    # item
    def delete_item(self, _item, tp_w):
        tp_w = list(tp_w.split())
        arr = self.posts.find_one()
        arr = list(arr.keys())
        self.posts.remove({arr[1]: _item, arr[3]: int(tp_w[0])})
        arr = [int(tp_w[0]), None]
        self.output(arr)

    def adding_item(self, _list):
        arr = list(self.posts.find_one().keys())
        new_posts = {
            arr[1]: _list[0],
            arr[2]: _list[1],
            arr[3]: _list[3],
            arr[4]: int(_list[2]),
        }
        self.posts.insert_one(new_posts)
        arr = [_list[3], None]
        self.output(arr)

    # outputs
    def output(self, value):
        arr = []
        arr.append(value[0])
        if value[0] == 0:
            _obj = self.pos_ad.find(value[1] if value[1] else None)
            for post in _obj:
                post = OrderedDict(post)
                arr.append(post)
            self.output_changed.emit(arr)
            return 0
        else:
            _obj = self.posts.find(value[1] if value[1] else {'warehouse': value[0]})
            for post in _obj:
                post = OrderedDict(post)
                arr.append(post)
            self.output_changed.emit(arr)
            return 0

    def type_w(self):
        arr = []
        _obj = self.tp_w.find()
        for post in _obj:
            arr.append(post)
        self.type_changed.emit(arr)

    def update_db(self, db):
        if db == 0:
            arr = [0, None]
            self.output(arr)
        else:
            arr = [db, None]
            self.output(arr)

    # type warehouse
    def drop_war(self, num):
        self.tp_w.remove({'number_w': num})
        self.posts.remove({'warehouse': num})
        self.type_w()

    def adding_war(self, value):
        self._count += 1
        self.tp_w.insert_one({'number_w': str(self._count), 'type_w': str(value)})
        self.type_w()

    def adding_department(self, value, dep, name):
        date = datetime.datetime.now()
        date = date.strftime("%d-%m-%Y")
        arr = list(self.doc.find_one().keys())
        for i in range(len(value)):
            item = value[i]
            self.doc.insert_one({arr[1]: name,
                                 arr[2]: dep,
                                 arr[3]: item[0],
                                 arr[4]: item[1],
                                 arr[5]: item[2],
                                 arr[6]: item[3],
                                 arr[7]: date})
            war = list(item[3].split())
            self.posts.update_one({"name": item[1], "provider": item[2], "warehouse": int(war[2])},
                               {'$inc': {"stack": -1}})
        arr = [1, None]
        self.output(arr)

    def Export_date(self, index):
        export = {}
        if index == 1:
            table = self.doc
        else:
            table = self.posts
        arr = list(table.find_one().keys())
        for i in range(len(arr)):
            if i != 0:
                get = table.find({arr[i]:{'$ne': ''}})
                list_item = []
                for row in get:
                    list_item.append(row[arr[i]])
                export[arr[i]] = list_item
        file = QFileDialog.getExistingDirectory()
        print(file)
        #file = QFileDialog.getOpenFileName(None, 'Open File', '/', "Excel Фаил (*.xlsx )")
        file = str(file)
        df = pd.DataFrame(export)
        df.to_excel(file+'./teams.xlsx')

    def Import_date(self,wh):
        wh = list(wh.split())
        wh = wh[0]
        file = QFileDialog.getOpenFileName(None, 'Open File', './', "Image (*.xlsx)")
        file = str(file[0])
        import_date = pd.read_excel(file)
        name = list(import_date.columns.ravel())
        name.pop(0)
        list_0 = import_date[name[0]].tolist()
        list_1 = import_date[name[1]].tolist()
        list_2 = import_date[name[3]].tolist()
        arr = list(self.posts.find_one().keys())
        for i in range(len(list_0)):
            new_posts = {
                arr[1]: list_0[i],
                arr[2]: list_1[i],
                arr[3]: int(wh),
                arr[4]: int(list_2[i]),
            }
            self.posts.insert_one(new_posts)
        arr = [int(wh), None]
        self.output(arr)


    def __init__(self):
        super().__init__()
        self.client = MongoClient() # Создание подключения к серверу
        self.db = self.client.warehouse
        self.posts = self.db.item_warehouse
        self.pos_ad = self.db.log_pas
        self.tp_w = self.db.type_warehouse
        self.doc = self.db.documents
        self.db.list_collection_names(include_system_collections=False)

        self._item = ""
        self._list = []
        self._count = self.tp_w.find().count()

        #self.pos_ad.remove({})
        if self.pos_ad.count() == 0:
            new_posts = {
                "name": "Admin",
                "status": "Admin",
                "login": "root",
                "password": "root"
            }
            self.posts.insert_one(new_posts)
        #self.posts.remove({})
        if self.posts.count() == 0:
            new_posts = {
                "name": "",
                "provider": "",
                "warehouse": "",
                "stack": ""
            }
            self.posts.insert_one(new_posts)
        #self.doc.remove({})
        if self.doc.count() == 0:
            new_posts = {"name_user": "",
                         "department": "",
                         "inventory": "",
                         "name_item": "",
                         "name_pr": "",
                         "warehouse": "",
                         "date": ""}
            self.doc.insert_one(new_posts)

