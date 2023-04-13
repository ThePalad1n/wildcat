import re


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BST:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.root = None
        self.height = 0
        self.size = 0

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
        
    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
            self.size += 1
            return
        current = self.root
        parent = None
        while current is not None:
            parent = current
            if data < current.data:
                current = current.left
            else:
                current = current.right
        if data < parent.data:
            parent.left = Node(data)
        else:
            parent.right = Node(data)
        self.size += 1
        self.height = max(self.height, self.get_height(self.root))

    def delete(self, data):
        self.root = self.delete_helper(self.root, data)
        self.size -= 1
        self.height = max(self.get_height(self.root), 0)

    def delete_helper(self, node, data):
        if node is None:
            return None
        if data < node.data:
            node.left = self.delete_helper(node.left, data)
        elif data > node.data:
            node.right = self.delete_helper(node.right, data)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                temp = self.get_min(node.right)
                node.data = temp.data
                node.right = self.delete_helper(node.right, temp.data)
        return node

    def get_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def search(self, data):
        current = self.root
        while current is not None:
            if data == current.data:
                return True
            elif data < current.data:
                current = current.left
            else:
                current = current.right
        return False

    def preorder_iterate(self, node):
        if node is not None:
            print(node.data, end=" ")
            self.preorder_iterate(node.left)
            self.preorder_iterate(node.right)

    def inorder_iterate(self, node):
        if node is not None:
            self.inorder_iterate(node.left)
            print(node.data, end=" ")
            self.inorder_iterate(node.right)

    def postorder_iterate(self, node):
        if node is not None:
            self.postorder_iterate(node.left)
            self.postorder_iterate(node.right)
            print(node.data, end=" ")

    def value_order_iterate(self, node):
        if node is not None:
            self.value_order_iterate(node.left)
            print(node.data, end=" ")
            self.value_order_iterate(node.right)

    def get_height(self, node):
        if node is None:
            return 0
        else:
            return 1 + max(self.get_height(node.left), self.get_height(node.right))
        
    def get_node_depth(self, root, target_node):
        if root is None:
            return None
        elif root == target_node:
            return 0
        else:
            left_depth = self.get_node_depth(root.left, target_node)
            if left_depth is not None:
                return left_depth + 1
            right_depth = self.get_node_depth(root.right, target_node)
            if right_depth is not None:
                return right_depth + 1
            return None


def evaluate(node):
    if node.left is None and node.right is None:
        return node.data.get_value(node.data.value)
    else:
        left = evaluate(node.left)
        right = evaluate(node.right)
        if node.data.token_type == "PLUS":
            return left + right
        elif node.data.token_type == "MINUS":
            return left - right
        elif node.data.token_type == "MULTIPLY":
            return left * right
        elif node.data.token_type == "DIVIDE":
            return left / right
        else:
            raise ValueError(f"Unknown operator {node.data.token_type}")

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




#with open('source_code.txt', 'r') as file:
 #   code = file.read()
# Test the lexer

bst = BST([])
bst.insert(50)
bst.insert(30)
bst.insert(70)
bst.insert(20)
bst.insert(40)
bst.insert(60)
bst.insert(80)

# print the tree using various traversal methods
print("Preorder traversal:")
bst.preorder_iterate(bst.root)
print("\nInorder traversal:")
bst.inorder_iterate(bst.root)
print("\nPostorder traversal:")
bst.postorder_iterate(bst.root)
print("\nValue order traversal:")
bst.value_order_iterate(bst.root)

# search for a node
print("\nSearch for 60:", bst.search(60))
print("Search for 10:", bst.search(10))

# delete a node and print the tree again
bst.delete(50)
print("After deleting 50:")
bst.inorder_iterate(bst.root)
print("\n")


code = "12.1 plus 34 times (56.0 minus 78.97 divide 90)"
input_string = code
tokens = lex(input_string)
print(tokens)
parser = BST(tokens)
root = parser.parse()
result = evaluate(root)
print(result)
