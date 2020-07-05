
# python imports
from typing import List

# lib imports

# project imports
from models import BaseEntityModel, ColumnSpec, ColumnType
import chatterbox_constants as c
import data_functions as df
from fn_format import trunc




class SnippetModel(BaseEntityModel):

    help = 'snippet'
    name_column = 'name'
    description_column = 'description'
    snippet_column = 'snippet'

    columns: List[ColumnSpec] = [
        ColumnSpec(key=name_column, data_type=ColumnType.str, label='Name', width=100, sortable=True, browseable=True,
                   format_fn=None),
        ColumnSpec(key=description_column, data_type=ColumnType.str, label='Description', width=100,
                   sortable=False, browseable=True,
                   format_fn=trunc),
        ColumnSpec(key=snippet_column, data_type=ColumnType.str, label='Snippet', width=100,
                   sortable=False, browseable=True,
                   format_fn=trunc)
    ]

    def __init__(self, subject_id: int):
        super().__init__(subject_id, self.columns, c.COLLECTION_NAME_SNIPPET)

    def make_new_record(self):
        return {c.FIELD_NAME_ID: None, 'subject_id': self.parent_key, self.name_column: '',
                self.description_column: '',
                self.snippet_column: ''}

    def get_records(self):
        return df.get_snippets_by_subject(self.parent_key)
