import re

categorized ={
'literals': [r'\d+|\'.*?\'|\".*?\"'],
'operators': [r'\plus|\minus|\times|\divide'],
'variables': [r'[a-zA-Z_][a-zA-Z0-9_]*'],
'reserved_words': ['when', 'orwhen', 'otherwise', 'loop', 'repeat', 'end'],
'data_types': ['INTEGER', 'DECIMAL', 'BOOLEAN'],
'logical_operators': [r'\and|\or|\not'],
'comparative_operators': [r'\is|\is\snot|\greater\sthan|\less\sthan|\greater\sthan\sor\sis|\less\sthan\sor\sis']
}

# Define token types
TOKEN_TYPES = [
    ("DECIMAL", r"\d+\.\d+"),
    ("INTEGER", r"\d+"),
    ("PLUS", r"plus"),
    ("MINUS", r"minus"),
    ("MULTIPLY", r"times"),
    ("DIVIDE", r"divide"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("WHITESPACE", r"\s+"),
    ("BOOLEAN", r"true|false"),
    ("IS", r"is"),
    ("ISNOT", r"is\snot"),
    ("GREATERTHAN", r"greater\sthan"),
    ("LESSTHAN", r"less\sthan"),
    ("GREATERTHANORIS", r"greater\sthan\sor\sis"),
    ("LESSTHANORIS", r"less\sthan\sor\sis"),
]

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = self.get_value(value)

    def get_value(self, value):
        if self.token_type == "INTEGER":
            return int(value)
        elif self.token_type == "DECIMAL":
            return float(value)
        elif self.token_type == "BOOLEAN":
            return value == "true"
        else:
            return value

    def __repr__(self):
        return f"Token({self.token_type}, {self.value})"

def lex(input_string):
    tokens = []
    position = 0

    while position < len(input_string):
        for token_type, pattern in TOKEN_TYPES:
            match = re.match(pattern, input_string[position:])
            if match:
                if token_type != "WHITESPACE":
                    tokens.append(Token(token_type, match.group(0)))
                position += match.end()
                break
        else:
            raise ValueError(f"Unexpected character at position {position}: {input_string[position]}")

    return tokens


with open('source_code.txt', 'r') as file:
    code = file.read()
# Test the lexer
input_string = code
tokens = lex(input_string)
print(tokens)
