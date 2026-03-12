class Node:
    """Вузол однозв'язного списку"""
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    """Кільцевий однозв'язний список"""
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, data):
        """Додавання елемента в кінець списку"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            new_node.next = self.head
            return
        
        self.tail.next = new_node
        self.tail = new_node
        self.tail.next = self.head

    def delete(self, key):
        """Вилучення елемента за значенням"""
        if not self.head:
            return
        if self.head.data == key:
            if self.head == self.tail:
                self.head = None
                self.tail = None
                return
            self.head = self.head.next
            self.tail.next = self.head
            return
        curr = self.head.next
        prev = self.head
        while curr != self.head:
            if curr.data == key:
                prev.next = curr.next
                if curr == self.tail:
                    self.tail = prev
                return
            prev = curr
            curr = curr.next

    def search(self, key):
        """Пошук за заданим ключем"""
        if not self.head:
            return False
        
        curr = self.head
        while True:
            if curr.data == key:
                return True
            curr = curr.next
            if curr == self.head:
                break
        return False

    def print_list(self):
        """Виведення списку на екран"""
        if not self.head:
            print("Список порожній")
            return
        
        elements = []
        curr = self.head
        while True:
            elements.append(str(curr.data))
            curr = curr.next
            if curr == self.head:
                break
        print(" -> ".join(elements) + " (back to start)")


def get_combined_sorted_list(list1, list2):

    list1.tail.next = list2.head
    list2.tail.next = list1.head
    list1.tail = list2.tail
    
    all_values = []

    curr = list1.head
    while True:
        all_values.append(curr.data)
        curr = curr.next
        if curr == list1.head:
            break
    
    all_values.sort()
    
    print("\nРезультат сортування за зростанням:")
    print(all_values)

# Тестування
list_a = CircularLinkedList()
list_b = CircularLinkedList()

# Заповнюємо списки
for val in [15, 2, 8]: list_a.add(val)
for val in [1, 20, 5]: list_b.add(val)

print("Список 1:")
list_a.print_list()
print("Список 2:")
list_b.print_list()

get_combined_sorted_list(list_a, list_b)