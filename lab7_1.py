from dataclasses import dataclass
from collections.abc import Callable

@dataclass(frozen=True)
class HashTableItem:
	key: int
	value: str | None = None

class OpenHashTable:
    def __init__(self, capacity: int = 26) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._table: list[list[HashTableItem]] = [[] for _ in range(capacity)]
        self._size = 0
    
    def _hash(self, key: object) -> int:
        return ord(key) %  self._capacity
    
    def insert(self, key: int, value: str | None = None) -> bool:
        index = self._hash(key)
        bucket = self._table[index]

        bucket.append(HashTableItem(key=key, value=value))
        self._size += 1
        return True
    
    def search(self, key: int) -> HashTableItem | None:
        index = self._hash(key)
        bucket = self._table[index]
        
        return bucket if bucket else None
    
    def delete(self, key: int) -> bool:
        index = self._hash(key)
        bucket = self._table[index]

        for i, item in enumerate(bucket):
            if item.key == key:
                del bucket[i]
                self._size -= 1
                return True
        return False
    
    @property
    def size(self) -> int:
        return self._size
    
    @property
    def capacity(self) -> int:
        return self._capacity
    
    def items(self) -> list[HashTableItem]:
        return [item for bucket in self._table for item in bucket]
    
    def __str__(self) -> str:
        rows: list[str] = []
        for index, bucket in enumerate(self._table):
            if not bucket:
                rows.append(f"{index:>2}: EMPTY")
            else:
                keys = ", ".join(str(item.key) for item in bucket)
                rows.append(f"{index:>2}: {keys}")
        return "\n".join(rows)
    



if __name__ == "__main__":
    user_string = input("Введіть рядок: ")
    hash_table = OpenHashTable()
    for char in user_string:
        hash_table.insert(char.lower())
    print("Хеш-таблиця створена:")
    print(str(hash_table))
    searched_letter = input("\nВведіть букву для пошуку: ")
    print(f"Кількість входжень букви '{searched_letter}': {
        len(hash_table.search(searched_letter.lower()))}")