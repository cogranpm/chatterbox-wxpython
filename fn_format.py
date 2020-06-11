""" functions for formatting data before displaying it etc """


def trunc(val: str) -> str:
    return reduce_characters(remove_newlines(val), 300)


def remove_newlines(val: str):
    return val.replace('\n', ' ')


def reduce_characters(val: str, max_length: int):
    if len(val) >= max_length:
        return val[0:(max_length - 1)] + ' ...'
    return val
