from tokenization.tools import *


class Token:
    def __init__(self, token_type, value):
        self.value = value

        self.group = token_type[0]
        self.sub_group = self.group + '-' + token_type[1]
        pass

    def __str__(self):
        return '{sub_type} {quotes}{value}{quotes}'.format(
            type=self.group,
            sub_type=self.sub_group,
            value=string_to_printable(self.value),
            quotes='`' if self.group == 'string' else ''
        )
