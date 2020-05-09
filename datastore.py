import dataset
import wx
import chatterbox_constants as c

class DataStore:

    def __init__(self):
        self.collections = dict()
        # wx.py.dispatcher.connect(receiver=self.store, signal=c.SIGNAL_STORE)
        wx.py.dispatcher.connect(receiver=self.shutdown, signal=c.SIGNAL_SHUTDOWN)
        wx.py.dispatcher.connect(receiver=self.create_entity, signal=c.SIGNAL_CREATE_ENTITY)
        self.db = dataset.connect('sqlite:///store.db')

    def shutdown(self, command, more):
        print(self.db.tables)
        self.db.close()

    def create_entity(self, command, more):
        name = more
        if name not in self.collections:
            #table = self.db.create_table(name, primary_id='id',
            #                             primary_type=self.db.types.bigint)
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

    def all(self, name):
        table = self.get_collection(name)
        if table is not None:
            return table.all()
        else:
            return dict()



