
from akindness.device_agnostic_file_storage.validation.character_level.charset import valid_characters
from akindness.device_agnostic_file_storage.validation.part_level.folder_structure import first_part_is_index
from akindness.device_agnostic_file_storage.validation.part_level.structure import has_parts, no_empty_parts, \
    parts_dont_start_with_underscore, parts_dont_end_with_underscore

validators = [
    valid_characters,
    has_parts,
    no_empty_parts,
    parts_dont_start_with_underscore,
    parts_dont_end_with_underscore,
    first_part_is_index
]

def get_all_validators():
    return tuple(validators)
