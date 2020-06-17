# -------- python imports -------------
from abc import ABCMeta, ABC, abstractmethod

# ---------- lib imports --------------
import wx.dataview as dv
import wx

# ---------- project imports -----------
# import views as v
import data_functions as df
import chatterbox_constants as c
import forms as frm
from models import BaseEntityModel
from views import BaseView


class BasePresenter(ABC):

    @staticmethod
    def start_editing(event):
        event.Veto()

    def __init__(self, parent: wx.Window, model: 'BaseEntityModel', view, form_def: frm.FormDef):
        self.parent = parent
        self.model = model
        self.view = view
        self.form_def = form_def

    def edited_record(self, record):
        self.model.ItemChanged(self.model.ObjectToItem(record))

    def update_data(self, data):
        self.model.change_data(data)

    def added_record(self, record):
        self.model.data.append(record)
        self.model.ItemAdded(dv.NullDataViewItem, self.model.ObjectToItem(record))


class PanelEditPresenter(BasePresenter):

    @staticmethod
    def start_editing(event):
        event.Veto()

    def __init__(self, parent: wx.Window, model: BaseEntityModel, view: BaseView, form_def: frm.FormDef):
        super().__init__(parent, model, view, form_def)
        self.view.set_list(self.model.columns)
        self.view.list.AssociateModel(self.model)
        self.model.DecRef()
        # required for linux, veto the editing event
        self.view.list.Bind(dv.EVT_DATAVIEW_ITEM_START_EDITING, self.start_editing)
        self.view.list.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, self.selection_handler)
        self.view.list.Bind(dv.EVT_DATAVIEW_ITEM_ACTIVATED, self.edit_handler)
        # form stuff
        self.view.set_form(self.form_def)
        self.model.change_data(self.model.create_data())
        # this next line must occur after the form_def is created
        self.set_view_state(c.ViewState.empty)
        wx.py.dispatcher.connect(receiver=self.save, signal=c.SIGNAL_SAVE)
        wx.py.dispatcher.connect(receiver=self.add, signal=c.SIGNAL_ADD)
        wx.py.dispatcher.connect(receiver=self.delete, signal=c.SIGNAL_DELETE)
        wx.py.dispatcher.send(signal=c.SIGNAL_VIEW_ACTIVATED, sender=self, command=c.COMMAND_VIEW_ACTIVATED, more=self)

    # handle the toolbar buttons
    def save(self, command, more):
        if more is self.view:
            if self.view_state == c.ViewState.adding:
                record = self.model.make_new_record()
                self.form_def.bind(record)
            if self.view.Validate():
                self.view.bind(c.BindDirection.from_window)
                if self.view_state == c.ViewState.adding:
                    self.added_record(record)
                    df.add_record(self.model.collection_name, record)
                else:
                    selected_item = self.view.list.GetSelection()
                    record = self.model.ItemToObject(selected_item)
                    df.update_record(self.model.collection_name, record)
                    self.edited_record(record)
                self.set_view_state(c.ViewState.loaded)

    def add(self, command, more):
        if more is self.view:
            self.set_view_state(c.ViewState.adding)

    def delete(self, command, more):
        if more is self.view:
            selected_item = self.view.list.GetSelection()
            if selected_item is not None:
                if frm.confirm_delete(self.view):
                    self.model.ItemDeleted(dv.NullDataViewItem, selected_item)
                    record = self.model.ItemToObject(selected_item)
                    df.delete_record(self.model.collection_name, record)
                    self.model.data.remove(record)
                    self.set_view_state(c.ViewState.empty)

    def set_view_state(self, state: c.ViewState):
        # need to update the form
        if state == c.ViewState.adding:
            self.form_def.reset_fields()
            self.form_def.enable_fields(True)
            self.form_def.setfocusfirst()
            wx.py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_ADDING, more=self)
        elif state == c.ViewState.empty:
            self.form_def.reset_fields()
            self.form_def.enable_fields(False)
            wx.py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_EMPTY, more=self)
        elif state == c.ViewState.loaded:
            self.form_def.enable_fields(True)
            self.form_def.setfocusfirst()
            wx.py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_LOADED, more=self)
            self.form_def.pause_dirty_events(False)
        elif state == c.ViewState.loading:
            self.form_def.pause_dirty_events(True)
        self.view_state = state


    def selection_handler(self, event):
        # not quite sure what to do, load the selection so it can be deleted?
        pass

    def edit_handler(self, event: dv.DataViewEvent):
        self.set_view_state(c.ViewState.loading)
        selected_item = self.view.list.GetSelection()
        record = self.model.ItemToObject(selected_item)
        # this sets the data property on all the validators that are defined for all the fields
        self.form_def.bind(record)
        # this tells view to push data from model to the controls
        self.view.bind(c.BindDirection.to_window)
        self.set_view_state(c.ViewState.loaded)


class ModalEditPresenter(BasePresenter):

    def __init__(self, parent: wx.Window, model: BaseEntityModel, view: BaseView, form_def: frm.FormDef):
        super().__init__(parent, model, view, form_def)
        self.view.set_list(self.model.columns)
        self.view.list.AssociateModel(self.model)
        self.model.DecRef()

