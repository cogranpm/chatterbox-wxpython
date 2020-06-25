# python imports
from typing import List
import datetime as dt

# lib imports


# project imports
from models import BaseEntityModel
from presenters import ModalEditPresenter
from views import ModalEditView
from fn_format import trunc
import forms as frm

import chatterbox_constants as c
import data_functions as df
from lists import ColumnType, ColumnSpec, publication_types
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

    def __init__(self, subject_id: int):
        super().__init__(subject_id, self.columns, c.COLLECTION_NAME_PUBLICATION)

    def make_new_record(self):
        return {c.FIELD_NAME_ID: None, 'subject_id': self.parent_key, self.name_column: '', self.description_column: '',
                self.type_column: '', self.created_column: dt.datetime.today()}

    def get_records(self):
        return df.get_publications_by_subject(self.parent_key)


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

    def __init__(self, parent):
        super().__init__(parent=parent,
                         model=PublicationModel(None),
                         view=PublicationView(parent),
                         form_def=self.form_def)

    def selection_handler(self, event):
        super().selection_handler(event)
        selected_item = self.view.list.GetSelection()
        if selected_item is not None:
            record = self.model.ItemToObject(selected_item)
            #self.grinder_presenter.parent_changed(record)

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


class PublicationView(ModalEditView):

    def __init__(self, parent):
        try:
            super().__init__(parent, "Subject")
        except BaseException as ex:
            print('Error in  __init__: ' + str(ex))

