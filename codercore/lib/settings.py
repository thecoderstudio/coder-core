import os

settings = dict()


def update_settings(settings_):
    settings_ = _set_environment_variables(settings_)
    settings.update(settings_)
    return settings


def _set_environment_variables(settings_):
    """Interpolates any environment variables if present."""

    settings_with_env_vars = {}
    for key, value in settings_.items():
        try:
            settings_with_env_vars[key] = os.path.expandvars(value)
        except TypeError:
            settings_with_env_vars[key] = value
    return settings_with_env_vars
