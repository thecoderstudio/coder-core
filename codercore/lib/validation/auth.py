from marshmallow import (fields, pre_load, validates_schema, Schema,
                         ValidationError)
from sqlalchemy.orm.exc import NoResultFound

from codercore.db.models.user import get_user_by_email
from codercore.lib.encrypt import compare_plaintext_to_hash
from codercore.lib.validation import CleanString


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = CleanString(required=True)

    @pre_load
    def strip_email(self, data, **kwargs):
        try:
            data['email'] = data['email'].lower().strip()
        except KeyError:
            pass
        return data

    @validates_schema
    def validate_password(self, data, **kwargs):
        try:
            user = get_user_by_email(data.get('email')).one()
            if not compare_plaintext_to_hash(
                    data['password'], user.password_hash, user.password_salt):
                raise ValidationError('')
        except (NoResultFound, ValidationError):
            raise ValidationError("Email address and password don't match",
                                  'password')
