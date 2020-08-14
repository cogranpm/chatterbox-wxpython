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
from snippet import SnippetHeaderPresenter
from fn_format import trunc
import forms as frm

import chatterbox_constants as c
import data_functions as df
from lists import ColumnType, ColumnSpec, get_selected_item, get_record_from_item
from forms import large
from validators import not_empty, FieldValidator
import fn_widget as w
from Exception import InvalidParentKeyError


class SubjectModel(BaseEntityModel):

    help = 'Subject'
    name_column = 'name'
    description_column = 'description'
    shelf_id_column = 'shelf_id'

    columns: List[ColumnSpec] = [
        ColumnSpec(key=name_column, data_type=ColumnType.str, label='Name', width=100, sortable=True, browseable=True,
                   format_fn=None),
        ColumnSpec(key=description_column, data_type=ColumnType.str, label='Description', width=100, sortable=False, browseable=True,
                   format_fn=trunc)
    ]

    def __init__(self):
        super().__init__(self.columns, c.COLLECTION_NAME_SUBJECT)

    def make_new_record(self, shelf_id: int):
        return {c.FIELD_NAME_ID: None, self.shelf_id_column: shelf_id, self.name_column: '', self.description_column: ''}

    def get_records(self, shelf_id: int):
        return df.get_subjects_by_shelf(shelf_id)


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

    def __init__(self, shelf_presenter, parent):
        super().__init__(parent=parent,
                         model=SubjectModel(),
                         view=SubjectView(parent),
                         form_def=self.form_def)

        self.shelf_presenter = shelf_presenter
        self.grinder_presenter = GrinderPresenter(self.view.notebook, self)
        self.publication_presenter = PublicationPresenter(self.view.notebook, self)
        self.snippet_header_presenter = SnippetHeaderPresenter(self.view.notebook, self)
        self.child_presenters = [self.grinder_presenter, self.publication_presenter, self.snippet_header_presenter]
        self.view.add_child_page(self.grinder_presenter.view, "Grinders", True)
        self.view.add_child_page(self.publication_presenter.view, "Publications", False)
        self.view.add_child_page(self.snippet_header_presenter.view, "Snippets", False)
        self.view.init_children()

        # load the initial data based on parent shelf selection
        shelf_record = self.shelf_presenter.get_selected_record()
        if shelf_record is not None:
            records = self.model.get_records(shelf_record[c.FIELD_NAME_ID])
            self.model.change_data(self.model.create_data(records))

    def selection_handler(self, event):
        super().selection_handler(event)
        record = get_record_from_item(self.model, get_selected_item(self.view.list))
        if record is not None:
            for presenter in self.child_presenters:
                presenter.parent_changed()

    def call_delete_query(self, record):
        df.delete_subject(record)
        for presenter in self.child_presenters:
            presenter.parent_deleted()

    def validate_record(self, record):
        if record[SubjectModel.shelf_id_column] is None:
            raise InvalidParentKeyError
        return super().validate_record(record)


    def parent_changed(self):
        shelf_record = self.shelf_presenter.get_selected_record()
        if shelf_record is None:
            return
        shelf_id = shelf_record[c.FIELD_NAME_ID]
        records = self.model.create_data(self.model.get_records(shelf_id))
        self.update_data(records)

    def add(self, event):
        shelf_record = self.shelf_presenter.get_selected_record()
        if shelf_record is None:
            return
        record = self.model.make_new_record(shelf_record[c.FIELD_NAME_ID])
        super().add_record(record)



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



