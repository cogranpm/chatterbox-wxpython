""" module for subject view
 """
# python imports
from typing import List

# lib imports
import wx

# project imports
from models import BaseEntityModel
from presenters import ModalEditPresenter
from views import ModalEditViewParent
from grinder import GrinderPresenter
from publication import PublicationPresenter
from fn_format import trunc
import forms as frm

import chatterbox_constants as c
import data_functions as df
from lists import ColumnType, ColumnSpec, get_selected_item, get_record_from_item
from forms import large
from validators import not_empty, FieldValidator
import fn_widget as w


class SubjectModel(BaseEntityModel):

    help = 'Subject'
    name_column = 'name'
    description_column = 'description'

    columns: List[ColumnSpec] = [
        ColumnSpec(key=name_column, data_type=ColumnType.str, label='Name', width=100, sortable=True, browseable=True,
                   format_fn=None),
        ColumnSpec(key=description_column, data_type=ColumnType.str, label='Description', width=100, sortable=False, browseable=True,
                   format_fn=trunc)
    ]

    def __init__(self, shelf_id: int):
        super().__init__(shelf_id, self.columns, c.COLLECTION_NAME_SUBJECT)

    def make_new_record(self):
        return {c.FIELD_NAME_ID: None, 'shelf_id': self.parent_key, self.name_column: '', self.description_column: ''}

    def get_records(self):
        return df.get_subjects_by_shelf(self.parent_key)


class SubjectPresenter(ModalEditPresenter):

    title: str = 'Subject'
    name_field_def: frm.EditFieldDef = frm.TextFieldDef(SubjectModel.name_column, large(), validator=FieldValidator(None, SubjectModel.name_column, [not_empty]))
    description_field_def: frm.EditFieldDef = frm.TextFieldDef(SubjectModel.description_column, large(),
                                                        validator=FieldValidator(None, SubjectModel.description_column,
                                                                                 []))
    edit_lines: List[frm.FormLineDef] = [frm.FormLineDef("Name", [name_field_def]), frm.FormLineDef("Description", [description_field_def])]
    form_def: frm.FormDef = frm.FormDef(title=title,
                                        help=SubjectModel.help,
                                        edit_lines=edit_lines,
                                        name='subject')

    def __init__(self, parent):
        super().__init__(parent=parent,
                         model=SubjectModel(None),
                         view=SubjectView(parent),
                         form_def=self.form_def)
        self.grinder_presenter = GrinderPresenter(self.view.notebook)
        self.publication_presenter = PublicationPresenter(self.view.notebook)
        self.child_presenters = [self.grinder_presenter, self.publication_presenter]
        self.view.add_child_page(self.grinder_presenter.view, "Grinders", True)
        self.view.add_child_page(self.publication_presenter.view, "Publications", False)
        self.view.init_children()

    def selection_handler(self, event):
        super().selection_handler(event)
        record = get_record_from_item(self.model, get_selected_item(self.view.list))
        if record is not None:
            for presenter in self.child_presenters:
                presenter.parent_changed(record)

    def call_delete_query(self, record):
        df.delete_subject(record)
        for presenter in self.child_presenters:
            presenter.parent_deleted()


class SubjectView(ModalEditViewParent):

    def __init__(self, parent):
        try:
            super().__init__(parent, "Subject")
            self.child_container = w.panel(self.splitter, [])
            self.child_container.SetSizer(frm.vsizer())
            self.notebook = w.notebook(self.child_container)
            self.child_container.Sizer.Add(self.notebook, wx.SizerFlags(1).Expand())
        except BaseException as ex:
            print('Error in  __init__: ' + str(ex))

    def init_children(self):
        self.splitter.SplitHorizontally(self.main_panel, self.child_container, 248)

    def add_child_page(self, view, caption: str, default: bool):
        self.notebook.AddPage(view, caption, default)


# class Subject:
#
#     def __init__(self, parent, parent_container, grinder: gr.Grinder):
#         self.parent = parent
#         self.grinder = grinder
#         self.shelf_id = None
#         self.list_spec = make_list_spec(fkey=self.shelf_id, selection_handler=self.__selection_change, edit_handler=self.__edit)
#         self.panel_spec = make_panel_spec(parent=parent_container, name='frmPanel', title=title,
#                                           collection_name=collection_name,
#                                           add_handler=self.__add, edit_handler=self.__edit)
#         self.panel = make_panel(self.panel_spec, self.list_spec)
#
#     # called from event on panel
#     def __add(self, event):
#         if self.shelf_id is None:
#             return
#         record = make_new_record(self.shelf_id)
#
#         dlg: FormDialog = make_dialog(parent=self.parent,
#                                              record=record, title=title, collection_name=collection_name)
#         form: FormSpec = self.__make_form(dialog=dlg, name=form_name,
#                                           record=record, form_title="Add " + title, helpstr=helpstr)
#         dlg.build(form)
#         result = dlg.ShowModal()
#         if result == wx.ID_OK:
#             df.add_record(collection_name, record)
#             self.list_spec.added_record(record)
#
#     def __edit(self, event):
#         selected_item = get_selected_item(self.panel.list)
#         record = get_record_from_item(self.list_spec.model, selected_item)
#         dlg: FormDialog = make_dialog(parent=self.parent,
#                                       record=record, title=title, collection_name=collection_name)
#         form: FormSpec = self.__make_form(dialog=dlg, name=form_name,
#                                           record=record, form_title="Edit " + title, helpstr=helpstr)
#         dlg.build(form)
#         result = dlg.ShowModal()
#         if result == wx.ID_OK:
#             df.update_record(collection_name, record)
#             self.list_spec.edited_record(record)
#
#     def __selection_change(self, event: dv.DataViewEvent):
#         selected_item = get_selected_item(self.panel.list)
#         if selected_item is not None:
#             record = get_record_from_item(self.list_spec.model, selected_item)
#             self.grinder.parent_changed(record[c.FIELD_NAME_ID])
#
#     def __make_form(self, dialog: FormDialog, name: str, record, form_title: str, helpstr: str):
#         form: FormSpec = FormSpec(parent=dialog, name=name, title=form_title, helpstr=helpstr, edit_lines=[
#             edit_line("Name", [TextField(name_column, large(),
#                                          validator=FieldValidator(record, name_column, [not_empty]))]),
#             edit_line("Description", [TextField(description_column, large(),
#                                                 validator=FieldValidator(record, description_column, [not_empty]))])
#         ])
#         return form
#
#     # comes from a list event
#     def parent_changed(self, fkey: int):
#         self.shelf_id = fkey
#         self.list_spec.update_data(create_data(fkey, df.get_subjects_by_shelf))
#
#
# def create_data(shelf_key, query_fn):
#     records = query_fn(shelf_key)
#     list = []
#     for record in records:
#         list.append(record)
#     return list
#
#
# def make_new_record(shelf_id: int):
#     return {'id': None, 'shelf_id': shelf_id, 'name': '', 'description': ''}
#
#
# def make_list_spec(fkey, selection_handler, edit_handler):
#     return ListSpec(columns=[
#         ColumnSpec(key=name_column, data_type=ColumnType.str, label='Name', width=100, sortable=True, browseable=True, format_fn=None),
#         ColumnSpec(key=description_column, data_type=ColumnType.str, label='Description', width=100, sortable=True, browseable=True, format_fn=None)
#     ], selection_handler=selection_handler,
#         edit_handler=edit_handler,
#         data=create_data(fkey, df.get_subjects_by_shelf))
#
#
#
