import copy


def check_required_field_errors(
    required_field_names: list[str], errors: list[dict]
) -> bool:
    errors = copy.deepcopy(errors)
    for required_field_name in required_field_names:
        i = _get_index_for_field_name(required_field_name, errors)
        if i == -1:
            return False
        del errors[i]
    return True


def _get_index_for_field_name(field_name: str, errors: list[dict]) -> int:
    for i, error in enumerate(errors):
        if error["loc"][-1] == field_name and error["type"] == "value_error.missing":
            return i
    return -1
