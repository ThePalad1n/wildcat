class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None
        self.height = 0
        self.size = 0
        
    def __init__(self, arr):
        self.root = None
        self.height = 0
        self.size = 0
        for i in arr:
            self.insert(i)

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
