""" functions with side effects for getting data """

import chatterbox_constants as c
from fn_app import get_data_store


def create_entity(collection_name: str):
    get_data_store().create_entity(collection_name)


def get_all(collection_name: str):
    return get_data_store().all(collection_name)


def delete_shelf(record):
    # need a cascading delete here
    # subjects
    subjects = get_subjects_by_shelf(record[c.FIELD_NAME_ID])
    for subject in subjects:
        delete_subject(subject)
    delete_record(c.COLLECTION_NAME_SHELF, record)


def delete_subject(record):
    grinders = get_grinders_by_subject(record[c.FIELD_NAME_ID])
    for grinder in grinders:
        delete_grinder(grinder)

    publications = get_publications_by_subject(c.FIELD_NAME_ID)
    for publication in publications:
        delete_publication(publication)

    snippet_headers = get_snippet_headers_by_subject(record[c.FIELD_NAME_ID])
    for snippet_header in snippet_headers:
        delete_snippet_header(snippet_header)
    delete_record(c.COLLECTION_NAME_SUBJECT, record)


def delete_grinder(record):
    grinder_tasks = get_grinder_tasks_by_grinder(record[c.FIELD_NAME_ID])
    for grinder_task in grinder_tasks:
        # delete the grinder_task
        delete_grinder_task(grinder_task)

    # delete the grinder
    delete_record(c.COLLECTION_NAME_GRINDER, record)


def delete_publication(record):
    # grinder_tasks = get_grinder_tasks_by_grinder(record[c.FIELD_NAME_ID])
    # for grinder_task in grinder_tasks:
    #     # delete the grinder_task
    #     delete_grinder_task(grinder_task)
    delete_record(c.COLLECTION_NAME_PUBLICATION, record)


def delete_grinder_task(record):
    delete_record(c.COLLECTION_NAME_GRINDERTASK, record)


def delete_snippet_header(record):
    snippets = get_snippet_by_snippet_header(record[c.FIELD_NAME_ID])
    for snippet in snippets:
        delete_snippet(snippet)
    delete_record(c.COLLECTION_NAME_SNIPPET_HEADER, record)


def delete_snippet(record):
    delete_record(c.COLLECTION_NAME_SNIPPET, record)


def get_subjects_by_shelf(shelf_id):
    return get_data_store().query(c.COLLECTION_NAME_SUBJECT, {'shelf_id': shelf_id})


def get_grinders_by_subject(subject_id):
    return get_data_store().query(c.COLLECTION_NAME_GRINDER, {'subject_id': subject_id})


def get_publications_by_subject(subject_id):
    return get_data_store().query(c.COLLECTION_NAME_PUBLICATION, {'subject_id': subject_id})


def get_snippet_headers_by_subject(subject_id):
    return get_data_store().query(c.COLLECTION_NAME_SNIPPET_HEADER, {'subject_id': subject_id})


def get_grinder_tasks_by_grinder(grinder_id):
    return get_data_store().query(c.COLLECTION_NAME_GRINDERTASK, {'grinder_id': grinder_id})


def get_snippet_by_snippet_header(snippet_header_id):
    return get_data_store().query(c.COLLECTION_NAME_SNIPPET, {'snippet_header_id': snippet_header_id})


def add_record(collection_name: str, record):
    get_data_store().add(collection_name, record)


def update_record(collection_name: str, record):
    get_data_store().update(collection_name, record)


def delete_record(collection_name: str, record):
    get_data_store().remove(collection_name, record)

