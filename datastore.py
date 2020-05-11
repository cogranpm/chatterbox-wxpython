import dataset
import wx
import chatterbox_constants as c
from typing import Dict


class DataStore:

    db: dataset.Database
    collections: Dict[str,  dataset.Table]

    def __init__(self):
        self.collections = dict()
        wx.py.dispatcher.connect(receiver=self.shutdown, signal=c.SIGNAL_SHUTDOWN)
        self.db = dataset.connect('sqlite:///store.db')

    def shutdown(self, command, more):
        # print(self.db.tables)
        self.db.close()

    def create_entity(self, name):
        if name not in self.collections:
            table = self.db.create_table(name)
            self.collections[name] = table

    def get_collection(self, name):
        return self.collections.get(name, None)

    def add(self, name, record):
        table = self.get_collection(name)
        if table is None:
            return
        id = table.insert(record)
        record[id] = id

    def update(self, name, record):
        table = self.get_collection(name)
        if table is None:
            return
        table.update(record, ['id'])

    def remove(self, name, record):
        table = self.get_collection(name)
        if table is None:
            return
        table.delete(id=record['id'])

    def all(self, name):
        table = self.get_collection(name)
        if table is not None:
            return table.all()
        else:
            return dict()



