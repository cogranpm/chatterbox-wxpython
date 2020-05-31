""" functions with side effects for getting data """

import chatterbox_constants as c
from fn_app import get_data_store

def get_subjects_by_shelfid(shelf_id):
    return get_data_store().query(c.COLLECTION_NAME_SUBJECT, {'shelf_id': shelf_id})

