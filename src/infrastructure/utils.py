import os
import re

from exception.generic_exception import GenericException
from infrastructure.log import Log

import unidecode


def to_kebab_case(input: str) -> str:
    """
    Convert a string to kebab case
    :param input: string to be converted
    :return: kebab case string
    """
    without_accent = unidecode.unidecode(input)
    underline_and_lower = without_accent.replace(" ", "_").lower()
    return re.sub(r"[\W]", "", underline_and_lower)


def _(value, default):
    """
    Return value if not None, otherwise return default
    :param value: value to be returned
    :param default: default value to be returned
    :return: value or default
    """
    return value if value else default


def split(value: str, splitter: str, default_for_empty=[]) -> list[str]:
    """
    Split a string by a splitter
    :param value: string to be split
    :param splitter: splitter
    :param default_for_empty: default value for empty string
    :return: list of strings
    """
    if not value or len(value) == 0 or value == splitter:
        return default_for_empty

    return value.split(splitter)


def join(value: list[str], joiner: str, default_for_empty=None) -> list[str]:
    """
    Join a list of strings by a joiner
    :param value: list of strings to be joined
    :param joiner: joiner
    :param default_for_empty: default value for empty list
    :return: joined string
    """
    if not value or len(value) == 0 or (len(value) == 1 and value[0] == ""):
        return default_for_empty

    return joiner.join(value)


def find_last_topic_number(text) -> int:
    """
    Find the last topic number in a text
    Given
        1. Objetivo:
        A página HTML permite...

        2. Interfaces de Usuário:
        2.1. Campo de Aluno:
    Returns 2

    :param text: text to be searched
    :return: last topic number
    """
    topics = re.findall(r'\n(\d+)', text)

    if topics:
        return int(topics[-1])
    else:
        return 0


def find_file_recursive(file_name: str, base_path: str, raise_error_msg: str | None = None, strip_base_path: bool = False) -> str | None:
    """
    Find a file recursively
    :param file_name: file name to be found
    :param base_path: base path to start the search
    :param raise_error_msg: error message to be raised if file not found, valid only if not None
    :param strip_base_path: strip base path from file found
    :return: file found
    """
    file_found: str | None = None
    for root, dirs, files in os.walk(base_path):
        if file_name in files:
            file_found = os.path.join(root, file_name)

    if file_found and strip_base_path:
        file_found = file_found.replace(base_path, "")
        if file_found.startswith(os.path.sep):
            file_found = file_found[1:]

    if not file_found and raise_error_msg:
        Log.error(raise_error_msg)
        raise GenericException(raise_error_msg)

    return file_found
