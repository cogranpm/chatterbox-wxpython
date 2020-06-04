""" functions with side effects for getting data """

import chatterbox_constants as c
from fn_app import get_data_store


def create_entity(collection_name: str):
    get_data_store().create_entity(collection_name)


def get_all(collection_name: str):
    return get_data_store().all(collection_name)


def get_subjects_by_shelf(shelf_id):
    return get_data_store().query(c.COLLECTION_NAME_SUBJECT, {'shelf_id': shelf_id})


def get_grinders_by_subject(subject_id):
    return get_data_store().query(c.COLLECTION_NAME_GRINDER, {'subject_id': subject_id})


def add_record(collection_name: str, record):
    get_data_store().add(collection_name, record)


def update_record(collection_name: str, record):
    get_data_store().update(collection_name, record)

