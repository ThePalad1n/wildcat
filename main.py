import re

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BSTParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def parse(self):
        root = self._parse_expression()
        if self.index < len(self.tokens):
            raise ValueError(f"Unexpected token {self.tokens[self.index]} at position {self.index}")
        return root

    def _parse_expression(self):
        left = self._parse_term()
        while self.index < len(self.tokens) and self.tokens[self.index].token_type in ["PLUS", "MINUS"]:
            op = self.tokens[self.index]
            self.index += 1
            right = self._parse_term()
            node = Node(op)
            node.left = left
            node.right = right
            left = node
        return left

    def _parse_term(self):
        left = self._parse_factor()
        while self.index < len(self.tokens) and self.tokens[self.index].token_type in ["MULTIPLY", "DIVIDE"]:
            op = self.tokens[self.index]
            self.index += 1
            right = self._parse_factor()
            node = Node(op)
            node.left = left
            node.right = right
            left = node
        return left

    def _parse_factor(self):
        if self.index >= len(self.tokens):
            raise ValueError(f"Unexpected end of expression")
        token = self.tokens[self.index]
        self.index += 1
        if token.token_type in ["INTEGER", "DECIMAL"]:
            return Node(token)
        elif token.token_type == "LPAREN":
            node = self._parse_expression()
            if self.tokens[self.index].token_type != "RPAREN":
                raise ValueError(f"Expected ) but got {self.tokens[self.index]} at position {self.index}")
            self.index += 1
            return node
        else:
            raise ValueError(f"Unexpected token {token} at position {self.index}")

def evaluate(node):
    if node.left is None and node.right is None:
        return node.value.get_value(node.value.value)
    else:
        left = evaluate(node.left)
        right = evaluate(node.right)
        if node.value.token_type == "PLUS":
            return left + right
        elif node.value.token_type == "MINUS":
            return left - right
        elif node.value.token_type == "MULTIPLY":
            return left * right
        elif node.value.token_type == "DIVIDE":
            return left / right
        else:
            raise ValueError(f"Unknown operator {node.value.token_type}")

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
parser = BSTParser(tokens)
root = parser.parse()
result = evaluate(root)
print(result)
