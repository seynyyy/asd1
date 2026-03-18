"""
Doubly Linked List Implementation with Variant 1 Solution

This module implements a doubly linked list data structure with methods for
insertion, deletion, searching, and a specific task to remove elements
following '&' characters.
"""


class Node:
    """
    Represents a single node in the doubly linked list.
    
    Attributes:
        value: The data stored in the node (typically a character).
        next: Pointer to the next node in the list.
        prev: Pointer to the previous node in the list.
    """
    
    def __init__(self, value):
        """Initialize a node with a given value."""
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """
    A doubly linked list implementation that maintains forward and backward
    traversal capabilities.
    """
    
    def __init__(self):
        """Initialize an empty doubly linked list with head pointer and count."""
        self.head = None
        self.count = 0  # Track the number of nodes in the list
    
    # ==================== Base Functionality ====================
    
    def push_front(self, value):
        """
        Adds an element to the beginning of the list.
        
        Time Complexity: O(1) - Constant time insertion at the front.
        
        Args:
            value: The value to add to the front of the list.
        """
        new_node = Node(value)
        
        if self.head is None:
            # List is empty
            self.head = new_node
        else:
            # Update pointers for the new node and current head
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        
        self.count += 1
    
    def push_back(self, value):
        """
        Adds an element to the end of the list.
        
        Time Complexity: O(n) - Linear time because we must traverse to the last node.
        
        Args:
            value: The value to add to the end of the list.
        """
        new_node = Node(value)
        
        if self.head is None:
            # List is empty
            self.head = new_node
        else:
            # Traverse to find the last node
            current = self.head
            while current.next is not None:
                current = current.next
            
            # Update pointers to add the new node at the end
            current.next = new_node
            new_node.prev = current
        
        self.count += 1
    
    def remove_node(self, node):
        """
        Removes a specific node from the list by updating its neighbors' pointers.
        
        Time Complexity: O(1) - Constant time removal when the node reference is known.
        
        Args:
            node: The node object to remove from the list.
        """
        if node is None:
            return
        
        # Case 1: Node is the head
        if node == self.head:
            self.head = node.next
            if self.head is not None:
                self.head.prev = None
        else:
            # Case 2: Node is not the head
            # Update the previous node's next pointer
            if node.prev is not None:
                node.prev.next = node.next
            
            # Update the next node's prev pointer
            if node.next is not None:
                node.next.prev = node.prev
        
        self.count -= 1
    
    def find(self, key):
        """
        Searches for a node by its value.
        
        Time Complexity: O(n) - Linear search through the list.
        
        Args:
            key: The value to search for.
        
        Returns:
            The Node object if found, None otherwise.
        """
        current = self.head
        while current is not None:
            if current.value == key:
                return current
            current = current.next
        return None
    
    
    def print_list(self):
        """
        Returns a string representation of the list to display its contents.
        
        Time Complexity: O(n) - Linear traversal to build the string.
        
        Returns:
            A string representation of the list in the format: value1 <-> value2 <-> value3
        """
        elements = []
        current = self.head
        while current is not None:
            elements.append(str(current.value))
            current = current.next
        return " <-> ".join(elements) if elements else "(empty list)"


# ==================== Variant 1: Remove element after '&' ====================

def solve_variant_1(dl_list):
    current = dl_list.head
    
    while current is not None:
        if current.value == '&':
            if current.next is not None:
                node_to_remove = current.next
                current.next = node_to_remove.next
                if node_to_remove.next is not None:
                    node_to_remove.next.prev = current
                dl_list.count -= 1
                current = current.next
            else:
                current = current.next
        else:
            current = current.next


# ==================== Variant 2: Insert 13.5 after first element > 2 ====================

def solve_variant_2(dl_list):
    current = dl_list.head
    while current is not None:
        if current.value > 2:
            new_node = Node(13.5)
            new_node.next = current.next
            new_node.prev = current
            if current.next is not None:
                current.next.prev = new_node
            current.next = new_node
            dl_list.count += 1
            return 
        current = current.next


# ==================== Example Usage and Testing ====================

if __name__ == "__main__":
    # Example 1: Basic operations
    print("=== Example 1: Basic Operations ===")
    dl_list = DoublyLinkedList()
    dl_list.push_back('H')
    dl_list.push_back('e')
    dl_list.push_back('l')
    dl_list.push_back('l')
    dl_list.push_back('o')
    print(f"List: {dl_list.print_list()}")
    print(f"Count: {dl_list.count}")
    
    # Example 2: push_front
    print("\n=== Example 2: push_front ===")
    dl_list.push_front('*')
    print(f"After push_front('*'): {dl_list.print_list()}")
    print(f"Count: {dl_list.count}")
    
    # Example 3: find and remove
    print("\n=== Example 3: find and remove ===")
    node_l = dl_list.find('l')
    if node_l:
        dl_list.remove_node(node_l)
        print(f"After removing first 'l': {dl_list.print_list()}")
        print(f"Count: {dl_list.count}")
    
    # Example 4: remove_node(head)
    print("\n=== Example 4: remove_node(head) ===")
    dl_list.remove_node(dl_list.head)
    print(f"After remove_node(head): {dl_list.print_list()}")
    print(f"Count: {dl_list.count}")
    
    # Example 5: Variant 1 - Remove after '&' (Characters)
    print("\n=== Example 5: Variant 1 - solve_variant_1() (Characters) ===")
    dl_list2 = DoublyLinkedList()
    chars = ['a', 'b', '&', 'c', 'd', '&', 'e', 'f']
    for char in chars:
        dl_list2.push_back(char)
    print(f"Original: {dl_list2.print_list()}")
    print(f"Count: {dl_list2.count}")
    solve_variant_1(dl_list2)
    print(f"After solve_variant_1(): {dl_list2.print_list()}")
    print(f"Count: {dl_list2.count}")
    
    # Example 6: Edge case - '&' at the end
    print("\n=== Example 6: Edge case - '&' at the end ===")
    dl_list3 = DoublyLinkedList()
    chars = ['x', 'y', 'z', '&']
    for char in chars:
        dl_list3.push_back(char)
    print(f"Original: {dl_list3.print_list()}")
    solve_variant_1(dl_list3)
    print(f"After solve_variant_1(): {dl_list3.print_list()}")
    
    # Example 7: Edge case - Multiple '&' in a row
    print("\n=== Example 7: Edge case - Multiple '&' in a row ===")
    dl_list4 = DoublyLinkedList()
    chars = ['p', 'q', '&', '&', 'r', 's']
    for char in chars:
        dl_list4.push_back(char)
    print(f"Original: {dl_list4.print_list()}")
    solve_variant_1(dl_list4)
    print(f"After solve_variant_1(): {dl_list4.print_list()}")
    
    # Example 8: Variant 2 - Insert 13.5 after first element > 2 (Real Numbers)
    print("\n=== Example 8: Variant 2 - solve_variant_2() (Real Numbers) ===")
    dl_list5 = DoublyLinkedList()
    numbers = [1.5, 2.0, 3.5, 4.2, 1.8]
    for num in numbers:
        dl_list5.push_back(num)
    print(f"Original: {dl_list5.print_list()}")
    print(f"Count: {dl_list5.count}")
    solve_variant_2(dl_list5)
    print(f"After solve_variant_2(): {dl_list5.print_list()}")
    print(f"Count: {dl_list5.count} (13.5 inserted after 3.5)")
    
    # Example 9: Edge case - No element > 2
    print("\n=== Example 9: Edge case - No element > 2 ===")
    dl_list6 = DoublyLinkedList()
    numbers = [0.5, 1.0, 1.5, 2.0]
    for num in numbers:
        dl_list6.push_back(num)
    print(f"Original: {dl_list6.print_list()}")
    solve_variant_2(dl_list6)
    print(f"After solve_variant_2(): {dl_list6.print_list()} (no insertion)")
    print(f"Count: {dl_list6.count}")

