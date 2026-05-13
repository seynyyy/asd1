class Node:
    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node

class Stack:
    def __init__(self):
        self.head = None
        self.count = 0

    def push(self, data):
        """Додавання елемента у вершину стека (LIFO)"""
        self.head = Node(data, self.head)
        self.count += 1

    def pop(self):
        """Вилучення елемента з вершини"""
        if self.head is None:
            return None
        data = self.head.data
        self.head = self.head.next
        self.count -= 1
        return data

    def display(self):
        """Відображення вмісту стека"""
        current = self.head
        elements = []
        while current:
            elements.append(str(current.data))
            current = current.next
        print("Стек (від вершини): " + " -> ".join(elements))

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def enqueue(self, data):
        """Додавання елемента в кінець черги (FIFO)"""
        new_node = Node(data)
        if self.count == 0:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.count += 1
        
    def dequeue(self):
        """Вилучення елемента з початку черги"""
        if self.head is None:
            return None
        data = self.head.data
        self.head = self.head.next
        self.count -= 1
        if self.count == 0:
            self.tail = None
        return data

    def display(self):
        """Відображення вмісту черги"""
        current = self.head
        elements = []
        while current:
            elements.append(str(current.data))
            current = current.next
        print("Черга (від голови до хвоста): " + " -> ".join(elements))
        
def solve_stack_task(stack):
    product = 1
    has_odd = False
    current = stack.head

    while current:
        if current.data % 2 != 0:
            product *= current.data
            has_odd = True
        current = current.next

    return product if has_odd else 0

def solve_queue_task(queue):
    positive_count = 0
    current = queue.head

    while current:
        if current.data > 0:
            positive_count += 1
        current = current.next

    return positive_count
    
if __name__ == "__main__":
    print("Завдання 1.1:")
    stack = Stack()
    numbers = [10, 3, 5, 8, 7]

    for num in numbers:
        stack.push(num)

    stack.display()

    result = solve_stack_task(stack)
    print(f"Добуток непарних значень: {result}")
    
    print("\nЗавдання 2.1:")
    queue = Queue()
    float_numbers = [-2.5, 3.1, 0.0, 4.8, -1.2, 7.3]

    for num in float_numbers:
        queue.enqueue(num)

    queue.display()
    result = solve_queue_task(queue)
    print(f"Кількість додатних елементів у черзі: {result}")