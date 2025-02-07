
from akindness.device_agnostic_file_storage.check.character_level.charset import valid_characters

check_methods = [
    valid_characters
]

def get_all_checks():
    return tuple(check_methods)
