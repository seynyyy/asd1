import random
from unittest import result


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        """Add a value to the tree."""
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        elif value >= node.value:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)

    def delete(self, value):
        """Remove a value from the tree."""
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        if node is None:
            return None

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            successor = self._find_min(node.right)
            node.value = successor.value
            node.right = self._delete_recursive(node.right, successor.value)

        return node

    def _find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def search(self, value):
        """Check whether a value exists in the tree."""
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        if node is None:
            return False
        if value == node.value:
            return True
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)

    def get_leaf_nodes(self):
        result = []
        self._get_leaves_recursive(self.root, result)
        return result

    def _get_leaves_recursive(self, node, result):
        if node is not None:
            if node.left is None and node.right is None:
                result.append(node.value)
            else:
                self._get_leaves_recursive(node.left, result)
                self._get_leaves_recursive(node.right, result)

    def display_tree(self):
        if self.root is None:
            print("Tree is empty")
        else:
            self._display_recursive(self.root, "", True)

    def _display_recursive(self, node, prefix, is_tail):
        if node is not None:
            connector = "`-- " if is_tail else "|-- "
            print(prefix + connector + str(node.value))

            children = []
            if node.left is not None:
                children.append((node.left, False))
            if node.right is not None:
                children.append((node.right, True))

            for child, last_child in children:
                next_prefix = prefix + ("    " if is_tail else "|   ")
                self._display_recursive(child, next_prefix, last_child)


def build_tree(values):
    tree = BinarySearchTree()
    for value in values:
        tree.insert(value)
    return tree



def preorder_recursive(node):
    if node is None:
        return 0
    
    return node.value + preorder_recursive(node.left) + preorder_recursive(node.right)

if __name__ == "__main__":
    print("Demonstration:")
    bst = build_tree([15, 7, 23, 4, 11, 19, 27, 2, 5, 9, 13])

    print("Tree structure:")
    bst.display_tree()

    search_values = [11, 8]
    for value in search_values:
        print(f"Search {value}: {'found' if bst.search(value) else 'not found'}")

    print(f"Leaf nodes: {bst.get_leaf_nodes()}")

    random_values = [random.randint(-50, 50) for _ in range(26)]
    random_tree = build_tree(random_values)
    print(f"Random values: {random_values}")
    print(f"Tree leaves: {random_tree.get_leaf_nodes()}")
    result = 0
    result = preorder_recursive(random_tree.root)
    
    print(f"Result of task: {result}")