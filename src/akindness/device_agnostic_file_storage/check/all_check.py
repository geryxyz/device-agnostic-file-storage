
from akindness.device_agnostic_file_storage.check.character_level.charset import valid_characters
from akindness.device_agnostic_file_storage.check.part_level.folder_structure import first_part_is_index
from akindness.device_agnostic_file_storage.check.part_level.structure import has_parts, no_empty_parts, \
    parts_dont_start_with_underscore, parts_dont_end_with_underscore

check_methods = [
    valid_characters,
    has_parts,
    no_empty_parts,
    parts_dont_start_with_underscore,
    parts_dont_end_with_underscore,
    first_part_is_index
]

def get_all_checks():
    return tuple(check_methods)
