
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


class SnippetHeaderModel(BaseEntityModel):
    help = 'Snippet Header'
    name_column = 'name'
    description_column = 'description'

    columns: List[ColumnSpec] = [
        ColumnSpec(key=name_column, data_type=ColumnType.str, label='Name', width=100, sortable=True, browseable=True,
                   format_fn=None),
        ColumnSpec(key=description_column, data_type=ColumnType.str, label='Description', width=100, sortable=False, browseable=True,
                   format_fn=trunc)
    ]

    def __init__(self, subject_id: int):
        super().__init__(subject_id, self.columns, c.COLLECTION_NAME_SNIPPET_HEADER)

    def make_new_record(self):
        return {c.FIELD_NAME_ID: None, 'subject_id': self.parent_key, self.name_column: '', self.description_column: ''}

    def get_records(self):
        return df.get_snippet_headers_by_subject(self.parent_key)


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

    def __init__(self, parent):
        super().__init__(parent=parent,
                         model=SnippetHeaderModel(None),
                         view=SnippetHeaderView(parent),
                         form_def=self.form_def)

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

    def __init__(self, snippet_header_id: int):
        super().__init__(snippet_header_id, self.columns, c.COLLECTION_NAME_SNIPPET)

    def make_new_record(self):
        return {c.FIELD_NAME_ID: None, 'snippet_header_id': self.parent_key, self.name_column: '',
                self.description_column: '',
                self.body_column: ''}

    def get_records(self):
        return df.get_snippet_by_snippet_header(self.parent_key)


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

    def __init__(self, parent_data, parent):
        form_def: frm.FormDef = frm.FormDef(title='Snippet',
                                                 help=SnippetModel.help,
                                                 edit_lines=self.edit_lines,
                                                 name='frmSnippet')
        super().__init__(parent=parent,
                         model=SnippetModel(parent_data[c.FIELD_NAME_ID]),
                         view=SnippetView(parent),
                         form_def=form_def)

    # these two look reusable in the base class
    def add(self, command, more):
        super().add(command, more)
        self.view.set_current_tab(self.edit_tab_index)

    def edit_handler(self, event: dv.DataViewEvent):
        super().edit_handler(event)
        self.view.set_current_tab(self.edit_tab_index)


class SnippetView(BaseViewNotebook):

    def __init__(self, parent):
        try:
            super().__init__(parent)
        except BaseException as ex:
            print('Error in SnippetView __init__: ' + str(ex))
