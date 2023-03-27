import re

# Define token types
TOKEN_TYPES = [
    ("NUMBER", r"\d+"),
    ("PLUS", r"plus"),
    ("MINUS", r"minus"),
    ("MULTIPLY", r"times"),
    ("DIVIDE", r"divide"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("WHITESPACE", r"\s+"),
]

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

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

# Test the lexer
input_string = "12 plus 34 times (56 minus 78 divide 90)"
tokens = lex(input_string)
print(tokens)
