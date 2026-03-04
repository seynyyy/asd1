import array
import tabulate

class DynamicArray:
    def __init__(self, capacity=0):
        self._size = 0
        self._capacity = max(1, capacity)
        self._array = array.array('d', [0.0] * self._capacity)

    def _resize(self, new_capacity):
        new_array = array.array('d', [0.0] * new_capacity)
        for i in range(self._size):
            new_array[i] = self._array[i]
        self._array = new_array
        self._capacity = new_capacity

    def append(self, value: float | list[float]):
        if isinstance(value, list):
            for v in value:
                if self._size == self._capacity:
                    self._resize(2 * self._capacity)
                self._array[self._size] = v
                self._size += 1
        else:
            if self._size == self._capacity:
                self._resize(2 * self._capacity)
            self._array[self._size] = value
            self._size += 1

    def insert(self, index, value): 
        if index < 0 or index > self._size:
            raise IndexError("Index out of range")
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        for i in range(self._size, index, -1): 
            self._array[i] = self._array[i - 1]
        self._array[index] = value
        self._size += 1

    def remove(self, index): 
        if self._size == 0: raise Exception("Array is empty")
        if index < 0 or index >= self._size: raise IndexError("Index out of range")
        for i in range(index + 1, self._size): 
            self._array[i-1] = self._array[i]
        self._size -= 1
        
    def get(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        return self._array[index]
    
    def find(self, value):
        for i in range(self._size):
            if self._array[i] == value:
                return i
        return -1

    def sum_of_negatives(self):
        return sum(x for x in self._array[:self._size] if x < 0)

    def product_between_min_max(self):
        if self._size < 3: return 0
    
        min_idx = max_idx = 0
        for i in range(1, self._size):
            if self._array[i] < self._array[min_idx]: min_idx = i
            if self._array[i] > self._array[max_idx]: max_idx = i
            
        start = min(min_idx, max_idx) + 1
        end = max(min_idx, max_idx)
        
        if start >= end: return 0
        
        res = 1.0
        for i in range(start, end):
            res *= self._array[i]
        return res

    def find_sequences(self):
        if self._size < 3: return []
        sequences = []
        count = 1
        for i in range(1, self._size):
            if self._array[i] == self._array[i-1]:
                count += 1
            else:
                if count >= 3:
                    sequences.append((self._array[i-1], count))
                count = 1
        if count >= 3:
            sequences.append((self._array[self._size-1], count))
        return sequences

    def __str__(self):
        return tabulate.tabulate([[i, self._array[i]] for i in range(self._size)], headers=["index", "value"], tablefmt="grid")

if __name__ == "__main__":
    arr = DynamicArray() 
    
    while True:
        try:
            exec(input("Enter command: "))
        except Exception as e:
            print(f"Error: {e}")