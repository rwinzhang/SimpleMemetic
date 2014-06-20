def prompt(message, default, validator=None):
    line = input(message)
    if line == '':
        return default

    value = type(default)(line)
    if validator:
        return value if validator(value) else prompt(message, default, validator)

    return value


def confirm(message):
    line = input(message).lower()
    return line == '' or line == 'y'
