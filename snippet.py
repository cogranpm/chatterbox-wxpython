
# python imports
from typing import List

# lib imports
import wx
import wx.dataview as dv

# project imports
from models import BaseEntityModel, ColumnSpec, ColumnType
import chatterbox_constants as c
import data_functions as df
from fn_format import trunc
from presenters import ModalEditPresenter, PanelEditPresenter
import forms as frm
from validators import FieldValidator, not_empty
from views import ModalEditView, BaseViewNotebook
from Exception import InvalidParentKeyError


class SnippetHeaderModel(BaseEntityModel):
    help = 'Snippet Header'
    name_column = 'name'
    description_column = 'description'
    subject_id_column = 'subject_id'

    columns: List[ColumnSpec] = [
        ColumnSpec(key=name_column, data_type=ColumnType.str, label='Name', width=100, sortable=True, browseable=True,
                   format_fn=None),
        ColumnSpec(key=description_column, data_type=ColumnType.str, label='Description', width=100, sortable=False, browseable=True,
                   format_fn=trunc)
    ]

    def __init__(self):
        super().__init__(self.columns, c.COLLECTION_NAME_SNIPPET_HEADER)

    def make_new_record(self, subject_id: int):
        return {c.FIELD_NAME_ID: None, self.subject_id_column: subject_id, self.name_column: '', self.description_column: ''}

    def get_records(self, subject_id: int):
        return df.get_snippet_headers_by_subject(subject_id)


class SnippetHeaderPresenter(ModalEditPresenter):

    title: str = 'Snippet Header'
    name_field_def: frm.EditFieldDef = frm.TextFieldDef(SnippetHeaderModel.name_column, frm.large(),
                                                        validator=FieldValidator(None, SnippetHeaderModel.name_column,
                                                                                 [not_empty]))
    description_field_def: frm.EditFieldDef = frm.TextFieldDef(SnippetHeaderModel.description_column, frm.large(),
                                                        validator=FieldValidator(None, SnippetHeaderModel.description_column,
                                                                                 []))
    edit_lines: List[frm.FormLineDef] = [frm.FormLineDef("Name", [name_field_def]),
                                         frm.FormLineDef("Description", [description_field_def])]
    form_def: frm.FormDef = frm.FormDef(title=title,
                                        help=SnippetHeaderModel.help,
                                        edit_lines=edit_lines,
                                        name='frmSnippetHeader')

    def __init__(self, parent, subject_presenter):
        super().__init__(parent=parent,
                         model=SnippetHeaderModel(),
                         view=SnippetHeaderView(parent),
                         form_def=self.form_def)
        self.subject_presenter = subject_presenter

    def selection_handler(self, event):
        pass

    def call_delete_query(self, record):
        df.delete_snippet_header(record)

    def bind_list_item_activated_event(self):
        self.view.list.Bind(dv.EVT_DATAVIEW_ITEM_ACTIVATED, self.edit_snippet)

    def edit_snippet(self, event):
        selected_item = self.view.list.GetSelection()
        record = self.model.ItemToObject(selected_item)
        presenter = SnippetPresenter(record, wx.GetApp().get_frame())
        wx.GetApp().get_frame().add_page(key="snippet", title=c.NOTEBOOK_TITLE_SNIPPET,
                                   window=presenter.view, page_data=None)

    def validate_record(self, record):
        if record(SnippetHeaderModel.subject_id_column) is None:
            raise InvalidParentKeyError
        return super().validate_record(record)


    def parent_changed(self):
        pass
        # shelf_record = self.get_shelf_record()
        # shelf_id = shelf_record[c.FIELD_NAME_ID]
        # records = self.model.create_data(self.model.get_records(shelf_id))
        # self.update_data(records)


class SnippetHeaderView(ModalEditView):

    def __init__(self, parent):
        try:
            super().__init__(parent, "Grinder")
        except BaseException as ex:
            print('Error in  __init__: ' + str(ex))


# --------------------------------------------------------------
# snippets
class SnippetModel(BaseEntityModel):

    help = 'snippet'
    name_column = 'name'
    description_column = 'description'
    body_column = 'body'
    snippet_header_column = 'snippet_header_id'

    columns: List[ColumnSpec] = [
        ColumnSpec(key=name_column, data_type=ColumnType.str, label='Name', width=100, sortable=True, browseable=True,
                   format_fn=None),
        ColumnSpec(key=description_column, data_type=ColumnType.str, label='Description', width=100,
                   sortable=False, browseable=True,
                   format_fn=trunc),
        ColumnSpec(key=body_column, data_type=ColumnType.str, label='Body', width=100,
                   sortable=False, browseable=True,
                   format_fn=trunc)
    ]

    def __init__(self):
        super().__init__(self.columns, c.COLLECTION_NAME_SNIPPET)

    def make_new_record(self, snippet_header_id: int):
        return {c.FIELD_NAME_ID: None, self.snippet_header_column: snippet_header_id, self.name_column: '',
                self.description_column: '',
                self.body_column: ''}

    def get_records(self, snippet_header_id: int):
        return df.get_snippet_by_snippet_header(snippet_header_id)


class SnippetPresenter(PanelEditPresenter):

    edit_tab_index = 1
    name_field_def: frm.EditFieldDef = frm.TextFieldDef(name=SnippetModel.name_column, width=frm.large(),
                                                        validator=FieldValidator(None, SnippetModel.name_column,
                                                                                 [not_empty]),
                                                        multi_line=False)
    description_field_def: frm.EditFieldDef = frm.TextFieldDef(name=SnippetModel.description_column, width=frm.large(),
                                                             validator=FieldValidator(
                                                                 None,
                                                                 SnippetModel.description_column,
                                                                 [not_empty]),
                                                               multi_line=True)

    body_field_def: frm.EditFieldDef = frm.CodeEditorDef(name=SnippetModel.body_column, width=frm.large(),
                                                                validator=FieldValidator(None,
                                                                                         SnippetModel.body_column,
                                                                                         [not_empty]))
    edit_lines: List[frm.FormLineDef] = [frm.FormLineDef("Name", [name_field_def]),
                                         frm.FormLineDef("Description", [description_field_def]),
                                         frm.FormLineDef("Body", [body_field_def])]

    def __init__(self, parent, snippet_header_presenter: SnippetHeaderPresenter):
        form_def: frm.FormDef = frm.FormDef(title='Snippet',
                                                 help=SnippetModel.help,
                                                 edit_lines=self.edit_lines,
                                                 name='frmSnippet')
        super().__init__(parent=parent,
                         model=SnippetModel(),
                         view=SnippetView(parent),
                         form_def=form_def)
        self.snippet_header_presenter = snippet_header_presenter

    # these two look reusable in the base class
    def add(self, command, more):
        super().add(command, more)
        self.view.set_current_tab(self.edit_tab_index)

    def edit_handler(self, event: dv.DataViewEvent):
        super().edit_handler(event)
        self.view.set_current_tab(self.edit_tab_index)

    def validate_record(self, record):
        if record[SnippetModel.snippet_header_column] is None:
            raise InvalidParentKeyError
        return super().validate_record(record)


class SnippetView(BaseViewNotebook):

    def __init__(self, parent):
        try:
            super().__init__(parent)
        except BaseException as ex:
            print('Error in SnippetView __init__: ' + str(ex))
