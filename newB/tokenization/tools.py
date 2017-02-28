def char_to_spec(char):
    if char == 'n':
        return '\n'

    if char == 't':
        return '\t'

    if char == 's':
        return ' '

    return char


def string_to_printable(text):
    return text.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t')


def index_any(text, characters):
    characterSet = set(characters)
    index = next((pos for pos, char in enumerate(text) if char in characterSet), None)
    if index is not None:
        return index
    
    return -1
