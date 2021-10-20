# python imports
from typing import List
import datetime as dt

# lib imports
import wx

# project imports
from models import BaseEntityModel
from presenters import ModalEditPresenter
from views import ModalEditView
from fn_format import trunc
import forms as frm

import chatterbox_constants as c
import data_functions as df
from lists import ColumnType, ColumnSpec, publication_types, get_selected_item, get_record_from_item
from forms import large
from validators import not_empty, FieldValidator


class PublicationModel(BaseEntityModel):

    help = 'Publication'
    name_column = 'name'
    description_column = 'description'
    type_column = 'type'
    created_column = 'created'

    columns: List[ColumnSpec] = [
        ColumnSpec(key=name_column, data_type=ColumnType.str, label='Name', width=100, sortable=True, browseable=True,
                   format_fn=None),
        ColumnSpec(key=description_column, data_type=ColumnType.str, label='Description', width=100, sortable=False, browseable=True,
                   format_fn=trunc),
        ColumnSpec(key=type_column, data_type=ColumnType.str, label='Description', width=100, sortable=True,
                   browseable=True,
                   format_fn=trunc),
        ColumnSpec(key=created_column, data_type=ColumnType.date, label='Created', width=300,
                   sortable=True, browseable=True, format_fn=None)
    ]

    def __init__(self):
        super().__init__(self.columns, c.COLLECTION_NAME_PUBLICATION)

    def make_new_record(self, subject_id: int):
        return {c.FIELD_NAME_ID: None, 'subject_id': subject_id, self.name_column: '', self.description_column: '',
                self.type_column: '', self.created_column: dt.datetime.today()}

    def get_records(self, subject_id: int):
        return df.get_publications_by_subject(subject_id)


class PublicationPresenter(ModalEditPresenter):

    title: str = 'Publication'
    name_field_def: frm.EditFieldDef = frm.TextFieldDef(PublicationModel.name_column, large(), validator=FieldValidator(None, PublicationModel.name_column, [not_empty]))
    description_field_def: frm.EditFieldDef = frm.TextFieldDef(PublicationModel.description_column, large(), validator=FieldValidator(None, PublicationModel.description_column, []))
    type_field_def: frm.EditFieldDef = frm.ComboFieldDef(PublicationModel.type_column, frm.medium(), publication_types,
                                                               validator=FieldValidator(None,
                                                                                        PublicationModel.type_column,
                                                                                        [not_empty]))
    edit_lines: List[frm.FormLineDef] = [frm.FormLineDef("Name", [name_field_def]), frm.FormLineDef("Description", [description_field_def]),
                                         frm.FormLineDef("Type", [type_field_def])]
    form_def: frm.FormDef = frm.FormDef(title=title,
                                        help=PublicationModel.help,
                                        edit_lines=edit_lines,
                                        name='publication')

    def __init__(self, parent, subject_presenter):
        super().__init__(parent=parent,
                         model=PublicationModel(),
                         view=PublicationView(parent),
                         form_def=self.form_def)
        self.subject_presenter = subject_presenter


    def selection_handler(self, event):
        super().selection_handler(event)
        selected_item = self.view.list.GetSelection()
        if selected_item is not None:
            record = self.model.ItemToObject(selected_item)

    def call_delete_query(self, record):
        df.delete_publication(record)

    def subject_deleted(self, subject_presenter):
        """ the parent entity, shelf has been deleted
        all dependent subjects must also be deleted
        as well as all children of subjects
        and if the lists are visible they need to be updated as well
        via the models
        """
        pass

    def parent_changed(self):
        subject_record = self.subject_presenter.get_selected_record()
        if subject_record is None:
            return
        subject_id = subject_record[c.FIELD_NAME_ID]
        records = self.model.create_data(self.model.get_records(subject_id))
        self.update_data(records)

    def add(self, event):
        subject_record = self.subject_presenter.get_selected_record()
        if subject_record is None:
            return
        record = self.model.make_new_record(subject_record[c.FIELD_NAME_ID])
        super().add_record(record)


class PublicationView(ModalEditView):

    def __init__(self, parent):
        try:
            super().__init__(parent, "Subject")
        except BaseException as ex:
            print('Error in  __init__: ' + str(ex))

