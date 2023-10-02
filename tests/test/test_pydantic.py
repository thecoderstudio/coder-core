from codercore.test.pydantic import (
    check_required_field_errors,
    check_validation_value_error,
)

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


def test_check_validation_value_error_expected(mocker):
    location = ("order_by",)
    message = "order_by must be one of ('id',)"
    input_ = "wrong"
    error = {
        "type": "value_error",
        "loc": location,
        "msg": f"Value error, {message}",
        "input": input_,
        "ctx": {"error": ValueError(message)},
        "url": "https://errors.pydantic.dev/2.4/v/value_error",
    }
    validation_error = mocker.MagicMock()
    validation_error.errors.return_value = [error]
    assert check_validation_value_error(validation_error, location, message, input_)


def test_check_validation_value_error_unexpected_error(mocker):
    location = ("order_by",)
    message = "order_by must be one of ('id',)"
    input_ = "wrong"
    error = {
        "type": "value_error",
        "loc": location,
        "msg": f"Value error, {message}",
        "input": "Something else",
        "ctx": {"error": ValueError(message)},
        "url": "https://errors.pydantic.dev/2.4/v/value_error",
    }
    validation_error = mocker.MagicMock()
    validation_error.errors.return_value = [error]
    assert not check_validation_value_error(validation_error, location, message, input_)


def test_check_validation_value_error_unexpected_errors_length(mocker):
    location = ("order_by",)
    message = "order_by must be one of ('id',)"
    input_ = "wrong"
    validation_error = mocker.MagicMock()
    validation_error.errors.return_value = []
    assert not check_validation_value_error(validation_error, location, message, input_)
