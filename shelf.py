""" all classes and functions pertaining to a shelf
shelf can have list of child subjects
subject can have child:
  shelves list - infinite recursion of subjects and shelves
  grinders - coding exercises with exercise and solution
    designed to be delivered randomly when user asks
  publications - topics, notes, exercises, audio recordings
  snippets - example code for anything
"""
# ---------- python imports -------------------
import logging
from typing import List

# ----------- lib imports --------------------
import wx
import wx.dataview as dv

# ----------- project imports ----------------
import chatterbox_constants as c
import forms as frm
from lists import states, ColumnSpec, ColumnType, ListSpec, create_data, get_selected_item, get_record_from_item
from validators import FieldValidator, CheckboxValidator, ComboValidator, not_empty
from forms import FormSpec, FormDialog, FormLineSpec, edit_line, large, TextField
import data_functions as df
from models import BaseEntityModel
from presenters import ModalEditPresenter
from views import ModalEditViewParent
from subject import SubjectPresenter
import fn_widget as w
from Exception import InvalidParentKeyError



class ShelfModel(BaseEntityModel):

    help = 'Shelf'
    name_column = 'name'

    columns: List[ColumnSpec] = [
        ColumnSpec(key=name_column, data_type=ColumnType.str, label='Name', width=100, sortable=True, browseable=True,
                   format_fn=None)
    ]

    def __init__(self):
        super().__init__(self.columns, c.COLLECTION_NAME_SHELF)

    def make_new_record(self):
        return {c.FIELD_NAME_ID: None, self.name_column: ''}

    def get_records(self):
        return df.get_all(self.collection_name)


class ShelfPresenter(ModalEditPresenter):

    title: str = 'Shelf'
    name_field_def: frm.EditFieldDef = frm.TextFieldDef(ShelfModel.name_column, large(), validator=FieldValidator(None, ShelfModel.name_column, [not_empty]))
    edit_lines: List[frm.FormLineDef] = [frm.FormLineDef("Name", [name_field_def])]
    form_def: frm.FormDef = frm.FormDef(title=title,
                                        help=ShelfModel.help,
                                        edit_lines=edit_lines,
                                        name='shelf')

    # the subject argument is temporary
    # should be created within the shelf presenter
    def __init__(self, frame):

        super().__init__(parent=frame,
                         model=ShelfModel(),
                         view=ShelfView(frame),
                         form_def=self.form_def)

        # set if we can "put" the subject in the child container
        self.subject_presenter = SubjectPresenter(self, self.view.subject_container)
        self.view.init_children()
        self.model.change_data(self.model.create_data(self.model.get_records()))


    def selection_handler(self, event):
        super().selection_handler(event)
        # print(get_record_from_item(self.model, get_selected_item(self.view.list)))
        self.subject_presenter.parent_changed()

    # replace this, need to pass on delete request to subject presenter
    def call_delete_query(self, record):
        df.delete_shelf(record)
        self.subject_presenter.parent_deleted()

    def add(self, event):
        record = self.model.make_new_record()
        super().add_record(record)



class ShelfView(ModalEditViewParent):
    """

    """
    def __init__(self, parent):
        try:
            super().__init__(parent, "Shelf")
            self.subject_container = w.panel(self.splitter, [])
            self.subject_container.SetSizer(frm.vsizer())
        except BaseException as ex:
            print('Error in  __init__: ' + str(ex))

    def init_children(self):
        self.splitter.SplitVertically(self.main_panel, self.subject_container, 248)



# ----------- old stuff -------------------------


# class MainPanel(wx.Panel):
#     """ shows a list of shelves and all the children """
#     def __init__(self, parent):
#         self.frame = parent
#         super().__init__(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
#         main_sizer = frm.vsizer()
#         self.SetSizer(main_sizer)
#
#         # splitter for shelf panel and subject panel
#         splitter = frm.splitter(self)
#
#         # a panel for subject and it's children
#         subject_container = w.panel(splitter, [])
#         subject_sizer = frm.vsizer()
#         subject_container.SetSizer(subject_sizer)
#         subject_splitter = w.splitter(subject_container)
#
#         # this stuff is all wrong
#         # the parent should own the children presenter
#         # and should provide a container into which the child view should insert itself
#         # Grinder
#         # self.__grinder = gr.Grinder(self, subject_container)
#         self.__grinder = gr.GrinderPresenter(subject_container, self.frame)
#
#         # subject
#         #self.__subject = sb.Subject(self, subject_splitter, self.__grinder)
#         self.__subject = sb.SubjectPresenter(subject_splitter, self.__grinder)
#
#         # shelf
#         # self.shelf = Shelf(self, splitter, self.__subject)
#         presenter = ShelfPresenter(splitter, self.__subject)
#
#         # subject children
#         subject_notebook = w.notebook(subject_splitter)
#         publications = wx.TextCtrl(subject_notebook, -1, "Publications", style=wx.TE_MULTILINE)
#         subject_notebook.AddPage(self.__grinder.view, "Grinders", False)
#         subject_notebook.AddPage(publications, "Publications")
#         subject_splitter.SplitHorizontally(self.__subject.view, subject_notebook, 248)
#         subject_sizer.Add(subject_splitter, wx.SizerFlags(1).Expand())
#         splitter.SplitVertically(presenter.view, subject_container, 248)
#         # splitter.SetMinimumPaneSize(200)
#         # splitter.SetSashGravity(0.5)
#         main_sizer.Add(splitter, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))
#
#         # no save required
#         # wx.py.dispatcher.connect(receiver=self.save, signal=c.SIGNAL_SAVE)
#         # py.dispatcher.connect(receiver=handle_tool_add, signal=c.SIGNAL_ADD)
#         # py.dispatcher.connect(receiver=handle_tool_delete, signal=c.SIGNAL_DELETE)
#         py.dispatcher.send(signal=c.SIGNAL_VIEW_ACTIVATED, sender=self, command=c.COMMAND_VIEW_ACTIVATED, more=self)
#



# class Shelf:
#
#     def __init__(self, parent, container, subject: sb.Subject):
#         self.parent = parent
#         self.subject = subject
#         self.list_spec = make_list_spec(selection_handler=self.__selection_change,
#                                         edit_handler=self.__edit)
#         self.panel_spec = make_panel_spec(parent=container, name='frmShelf', title=title,
#                                           collection_name=collection_name,
#                                           add_handler=self.__add, edit_handler=self.__edit)
#         self.panel = make_panel(self.panel_spec, self.list_spec)
#         # called from event on panel
#
#     def __add(self, event):
#         record = make_new_record()
#         dlg: FormDialog = frm.make_dialog(parent=self.parent,
#                                       record=record, title=title, collection_name=collection_name)
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
#         dlg: FormDialog = frm.make_dialog(parent=self.parent,
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
#             self.subject.parent_changed(record[c.FIELD_NAME_ID])
#
#     def __make_form(self, dialog: FormDialog, name: str, record, form_title: str, helpstr: str):
#         form: FormSpec = FormSpec(parent=dialog, name=name, title=form_title, helpstr=helpstr, edit_lines=[
#             edit_line("Name", [TextField(name_column, large(),
#                                          validator=FieldValidator(record, name_column, [not_empty]))])
#         ])
#         return form
#
#
# def make_list_spec(selection_handler, edit_handler):
#     return ListSpec(columns=[
#         ColumnSpec(key=name_column, data_type=ColumnType.str, label='Name', width=100, sortable=True, browseable=True, format_fn=None)
#     ], selection_handler=selection_handler,
#         edit_handler=edit_handler,
#         data=create_data(df.get_all(collection_name)))
#

# def handle_tool_add():
#     focussed_item = wx.Window.FindFocus()
#     match = frm.is_child_of([panel, sb.panel], focussed_item)
#     if match is not None:
#         if match is sb.panel:
#             pass
#         elif match is panel:
#             pass
#
#
# def handle_tool_delete(self):
#     logging.info("delete tool item clicked")

