from tokenization.tools import *


class Token:
    def __init__(self, token_type, value):
        self.value = value

        self.type = token_type
        pass

    def __str__(self):
        return '{type} {quotes}{value}{quotes}'.format(
            type=self.type,
            value=string_to_printable(self.value),
            quotes='`' if self.type == 'string' else ''
        )
