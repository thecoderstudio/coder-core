import bleach
from marshmallow.fields import String


class CleanString(String):
    def __init__(self, capitalize=False, **kwargs):
        super(CleanString, self).__init__(**kwargs)
        self.capitalize = capitalize

    def _deserialize(self, value, attr, data, **kwargs):
        string = super()._deserialize(value, attr, data, **kwargs)
        if self.capitalize and len(string):
            string = string[0].capitalize(
            ) if len == 1 else string[0].capitalize() + string[1:]
        return bleach.clean(string, tags=[], strip=True)
