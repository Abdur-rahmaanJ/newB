import string
from tokenization.token import Token


class Tokenizer:
    def __init__(self):
        self.code = ''
        self.tokens = []
        self.position = 0

        self.parsers = [
            # Basic types parser
            self.__parse_number,
            self.__parse_character,
            self.__parse_string,

            # Identities parser
            self.__parse_identity,

            # Operators parser
            self.__parse_math_operator,
            self.__parse_comparison_operator,
            self.__parse_special_operator
        ]

        self.keywords = [
            'for', 'while', 'repeat',
            'if', 'then', 'else', 'endif',
        ]
        self.math_operators = '=+-*/^%()'
        self.comparison_operators = '<>!='
        self.special_operators = '.,[]{}'
        pass

    def tokenize(self, code, whitespace=False):
        self.code = code
        tok = self.next_token(whitespace)
        while tok:
            yield tok
            tok = self.next_token(whitespace)

        return True

    def next_token(self, whitespaces):
        if self.position >= len(self.code):
            return False

        tok = self.__parse_whitespace()
        while tok:
            self.position += 1
            if whitespaces:
                return tok
            tok = self.__parse_whitespace()

        for parse_function in self.parsers:
            tok = parse_function()
            if tok is False:
                raise ValueError(
                    'Tokenizer was unable to parse token `{}`'.format(
                        parse_function.__name__.replace('parse', '').lstrip('_')
                    )
                )
            if tok:
                self.position += 1
                return tok

        raise ValueError(
            'Tokenizer was unable to parse token at position `{}`.\nCode part: {}'.format(
                self.position,
                self.code[
                    self.position:
                    self.position + index_any(self.code[self.position:], ' \r\t\n') - 1
                ]
            )
        )

    def add_parser(self, parse_function):
        if not callable(parse_function):
            raise TypeError(
                'parse_function expected to be callable(function), but `{type}` was given'.format(
                    type=type(parse_function).__name__
                )
            )

        self.parsers.insert(0, parse_function)
        return

    def __parse_whitespace(self):
        if not self.code[self.position].isspace():
            return None

        start = self.position
        self.position += 1

        while self.position < len(self.code):
            if self.code[self.position].isspace():
                self.position += 1
                continue

            break

        self.position -= 1
        return Token(('whitespace', 'whitespace'), self.code[start:self.position + 1])

    def __parse_number(self):
        if self.code[self.position] not in string.digits:
            return None

        start = self.position
        self.position += 1

        is_integer = True
        while self.position < len(self.code):
            symbol = self.code[self.position]
            if symbol in string.digits:
                self.position += 1
                continue

            if symbol == '.' and is_integer:
                is_integer = False

                if self.position + 1 < len(self.code) and self.code[self.position + 1] in string.digits:
                    self.position += 2
                    continue

            break

        self.position -= 1
        return Token(('number', 'integer' if is_integer else 'float'), self.code[start:self.position + 1])

    def __parse_character(self):
        if self.code[self.position] != '\'':
            return None

        self.position += 1
        if self.position >= len(self.code):
            return False

        if self.code[self.position] == '\\':
            self.position += 1

            if self.position >= len(self.code):
                return False

            symbol = char_to_spec(self.code[self.position])
            symbol_type = 'special'
            if symbol == self.code[self.position]:
                symbol_type = 'normal'
            return Token(('character', symbol_type), symbol)

        return Token(('character', 'normal'), self.code[self.position])

    def __parse_string(self):
        if self.code[self.position] != '"':
            return None

        data = ''
        self.position += 1
        while self.position < len(self.code):
            symbol = self.code[self.position]

            if symbol == '\\':
                self.position += 1
                if self.position >= len(self.code):
                    return False

                symbol = char_to_spec(symbol)
            elif symbol == '"':
                return Token(('string', 'normal'), data)

            data += symbol
            self.position += 1

        return False

    def __parse_identity(self):
        symbol = self.code[self.position]
        if symbol not in string.ascii_letters and symbol != '_':
            return None

        start = self.position
        self.position += 1
        while self.position < len(self.code):
            symbol = self.code[self.position]
            if symbol in string.ascii_letters or symbol in string.digits or symbol == '_':
                self.position += 1
                continue

            break

        tok = self.code[start:self.position]
        token_type = 'identity'
        if tok in self.keywords:
            token_type = 'keyword'

        self.position -= 1
        return Token(('identity', token_type), tok)

    def __parse_math_operator(self):
        symbol = self.code[self.position]
        if symbol in self.math_operators:
            return Token(('operator', 'math'), symbol)

        return None

    def __parse_comparison_operator(self):
        symbol = self.code[self.position]
        if symbol in self.comparison_operators:
            return Token(('operator', 'comparison'), symbol)

        return None

    def __parse_special_operator(self):
        symbol = self.code[self.position]
        if symbol in self.special_operators:
            return Token(('operator', 'special'), symbol)

        return None
