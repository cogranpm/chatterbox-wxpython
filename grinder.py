"""
module for grinders view
a grinder is an exercise to practice something
this ui is for navigating the grinders for a particular subject
"""
# ----------- python imports ---------------------
from typing import Callable, Dict, List
from enum import IntEnum

# ----------- lib imports ------------------------
import wx
import wx.dataview as dv
import datetime as dt

# ----------- project imports ---------------------
import chatterbox_constants as c
import data_functions as df
import views as v
from lists import ListSpec, ColumnType, ColumnSpec, get_selected_item, get_record_from_item
from panels import PanelSpec, BasePanel
import forms as frm
from validators import not_empty, FieldValidator
from models import BaseEntityModel
from presenters import PanelEditPresenter
import fn_format as fmt

from models import BaseEntityModel
from presenters import ModalEditPresenter
from views import ModalEditView
from fn_format import trunc

name_column = 'name'
description_column = 'description'
helpstr = "Grinders ..."
title = "Grinders"
form_name = "frmGrinder"
collection_name = c.COLLECTION_NAME_GRINDER


def create_data(subject_id, query_fn):
    records = query_fn(subject_id)
    list = []
    for record in records:
        list.append(record)
    return list


def make_new_record(subject_id: int):
    return {'id': None, 'subject_id': subject_id, 'name': '', 'description': ''}


def make_list_spec(fkey: int, selection_handler: Callable, edit_handler: Callable):
    return ListSpec(columns=[
        ColumnSpec(key=name_column, data_type=ColumnType.str, label='Name', width=100, sortable=True, browseable=True, format_fn=None),
        ColumnSpec(key=description_column, data_type=ColumnType.str, label='Description', width=100, sortable=True, browseable=True, format_fn=None)
    ], selection_handler=selection_handler,
        edit_handler=edit_handler,
        data=create_data(fkey, df.get_grinders_by_subject))


def make_panel_spec(parent, add_handler: Callable, edit_handler: Callable):
    return PanelSpec(parent=parent, name="pnlGrinder", title=title,
                     collection_name=collection_name, add_handler=add_handler, edit_handler=edit_handler)


def make_panel(spec: PanelSpec, list_spec: ListSpec):
    return BasePanel(spec=spec, listspec=list_spec)


def selection_change(event):
    pass


class Grinder:

    def __init__(self, parent, container):
        self.parent = parent
        self.container = container
        self.fkey = None
        self.__list_spec = make_list_spec(self.fkey, selection_change, self.__edit)
        self.__panel_spec = make_panel_spec(container, self.__add, self.__edit)
        self.panel = make_panel(self.__panel_spec, self.__list_spec)

    def parent_changed(self, fkey: int):
        self.fkey = fkey
        self.__list_spec.update_data(create_data(self.fkey, df.get_grinders_by_subject))


    def __make_form(self, dialog: frm.FormDialog, name: str, record, form_title: str, helpstr: str):
        form: frm.FormSpec = frm.FormSpec(parent=dialog, name=name, title=form_title, helpstr=helpstr, edit_lines=[
            frm.edit_line("Name", [frm.TextField(name_column, frm.large(),
                                         validator=FieldValidator(record, name_column, [not_empty]))]),
            frm.edit_line("Description", [frm.TextField(description_column, frm.large(),
                                                validator=FieldValidator(record, description_column, [not_empty]))])
        ])
        return form

    def __edit(self, event):
        # need to access the notebook and add a new page with a grindertask loaded as the child
        selected_item = get_selected_item(self.panel.list)
        record = get_record_from_item(self.__list_spec.model, selected_item)
        presenter = GrinderTaskPresenter(self, record, self.parent.frame)
        self.parent.frame.add_page(key="grinder_task", title=c.NOTEBOOK_TITLE_GRINDER,
                                   window=presenter.view, page_data=None)

    def __add(self, event):
        if self.fkey is None:
            return
        record = make_new_record(self.fkey)

        dlg: frm.FormDialog = frm.make_dialog(parent=self.parent,
                                             record=record, title=title, collection_name=collection_name)
        form: frm.FormSpec = self.__make_form(dialog=dlg, name=form_name,
                                          record=record, form_title="Add " + title, helpstr=helpstr)
        dlg.build(form)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            df.add_record(collection_name, record)
            self.__list_spec.added_record(record)


class GrinderModel(BaseEntityModel):

    help = 'Grinder'
    name_column = 'name'
    description_column = 'description'

    columns: List[ColumnSpec] = [
        ColumnSpec(key=name_column, data_type=ColumnType.str, label='Name', width=100, sortable=True, browseable=True,
                   format_fn=None),
        ColumnSpec(key=description_column, data_type=ColumnType.str, label='Description', width=100, sortable=False, browseable=True,
                   format_fn=trunc)
    ]

    def __init__(self, subject_id: int):
        super().__init__(subject_id, self.columns, c.COLLECTION_NAME_GRINDER)

    def make_new_record(self):
        return {c.FIELD_NAME_ID: None, 'subject_id': self.parent_key, self.name_column: '', self.description_column: ''}

    def get_records(self):
        return df.get_grinders_by_subject(self.parent_key)


class GrinderPresenter(ModalEditPresenter):

    title: str = 'Grinder'
    name_field_def: frm.EditFieldDef = frm.TextFieldDef(GrinderModel.name_column, frm.large(), validator=FieldValidator(None, GrinderModel.name_column, [not_empty]))
    description_field_def: frm.EditFieldDef = frm.TextFieldDef(GrinderModel.description_column, frm.large(),
                                                        validator=FieldValidator(None, GrinderModel.description_column,
                                                                                 []))
    edit_lines: List[frm.FormLineDef] = [frm.FormLineDef("Name", [name_field_def]), frm.FormLineDef("Description", [description_field_def])]
    form_def: frm.FormDef = frm.FormDef(title=title,
                                        help=GrinderModel.help,
                                        edit_lines=edit_lines,
                                        name='subject')

    def __init__(self, parent, frame):
        self.frame = frame
        super().__init__(parent=parent,
                         model=GrinderModel(None),
                         view=GrinderView(parent),
                         form_def=self.form_def)

    def selection_handler(self, event):
        pass
        # super().selection_handler(event)
        # selected_item = self.view.list.GetSelection()
        # if selected_item is not None:
        #     record = self.model.ItemToObject(selected_item)
        #     self.grinder.parent_changed(record[c.FIELD_NAME_ID])

    def call_delete_query(self, record):
        df.delete_grinder(record)

    def edit(self, event):
        selected_item = self.view.list.GetSelection()
        record = self.model.ItemToObject(selected_item)
        presenter = GrinderTaskPresenter(self, record, self.frame)
        self.frame.add_page(key="grinder_task", title=c.NOTEBOOK_TITLE_GRINDER,
                                   window=presenter.view, page_data=None)


class GrinderView(ModalEditView):

    def __init__(self, parent):
        try:
            super().__init__(parent, "Grinder")
        except BaseException as ex:
            print('Error in  __init__: ' + str(ex))



class GrinderTaskModel(BaseEntityModel):

    task_column = 'task'
    solution_column = 'solution'
    created_column = 'created'
    help = 'Grinder Task'

    columns: List[ColumnSpec] = [
        ColumnSpec(key=task_column, data_type=ColumnType.str, label='Task', width=400, sortable=True,
                   browseable=True, format_fn=fmt.trunc),
        ColumnSpec(key=solution_column, data_type=ColumnType.str, label='Solution', width=100,
                   sortable=False, browseable=False, format_fn=fmt.trunc),
        ColumnSpec(key=created_column, data_type=ColumnType.date, label='Created', width=300,
                   sortable=True, browseable=True, format_fn=None)
    ]

    def __init__(self, parent_key: int):
        super().__init__(parent_key, self.columns, c.COLLECTION_NAME_GRINDERTASK)

    def make_new_record(self):
        return {c.FIELD_NAME_ID: None, 'grinder_id': self.parent_key, self.task_column: '',
                self.solution_column: '', self.created_column: dt.datetime.today()}

    def get_records(self):
        return df.get_grinder_tasks_by_grinder(self.parent_key)


class GrinderTaskPresenter(PanelEditPresenter):

    edit_tab_index = 1
    task_field_def: frm.EditFieldDef = frm.TextFieldDef(name=GrinderTaskModel.task_column, width=frm.large(),
                                                        validator=FieldValidator(None, GrinderTaskModel.task_column,
                                                                                 [not_empty]),
                                                        multi_line=True)
    solution_field_def: frm.EditFieldDef = frm.CodeEditorDef(name=GrinderTaskModel.solution_column, width=frm.large(),
                                                             validator=FieldValidator(None,
                                                                                      GrinderTaskModel.solution_column,
                                                                                      [not_empty]))
    edit_lines: List[frm.FormLineDef] = [frm.FormLineDef("Task", [task_field_def]),
                                         frm.FormLineDef("Solution", [solution_field_def])]

    def __init__(self, grinder: Grinder, grinder_data, parent):
        form_def: frm.FormDef = frm.FormDef(title='Grinder Task',
                                                 help=GrinderTaskModel.help,
                                                 edit_lines=self.edit_lines,
                                                 name='frmGrinderTask')
        super().__init__(parent=parent,
                         model=GrinderTaskModel(grinder_data[c.FIELD_NAME_ID]),
                         view=GrinderTaskView(parent),
                         form_def=form_def)
        # self.Grinder = grinder
        # self.grinder_data = grinder_data


    def add(self, command, more):
        super().add(command, more)
        self.view.set_current_tab(self.edit_tab_index)

    def edit_handler(self, event: dv.DataViewEvent):
        super().edit_handler(event)
        self.view.set_current_tab(self.edit_tab_index)




class GrinderTaskView(v.BaseViewNotebook):
    """ has a list of grinder tasks - such as ;
    write an abstract base class etc etc
    each task needs to have a text solution
    hints?
    This class forms the View
    """

    def __init__(self, parent):
        try:
            super().__init__(parent)
        except BaseException as ex:
            print('Error in GrindTask __init__: ' + str(ex))



