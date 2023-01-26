from codercore.test.pydantic import check_required_field_errors

ERRORS = [
    {"loc": ["field_a"], "type": "value_error.missing"},
    {"loc": ["nested", "field_b"], "type": "value_error.missing"},
    {"loc": ["field_c"], "type": "type_error"},
]


def test_check_required_field_errors_true():
    required_fields = ["field_a", "field_b"]
    assert check_required_field_errors(required_fields, ERRORS)


def test_check_required_field_errors_wrong_type():
    required_fields = ["field_c"]
    assert not check_required_field_errors(required_fields, ERRORS)


def test_check_required_field_errors_missing():
    required_fields = ["field_d"]
    assert not check_required_field_errors(required_fields, ERRORS)
