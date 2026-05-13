"""Лабораторна робота 7: хеш-таблиця із закритим хешуванням.

У таблиці зберігаються 6-значні номери пристроїв формату 6xx1xx,
де кожен `x` означає будь-яку цифру від 0 до 9.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass


DEVICE_NUMBER_PATTERN = re.compile(r"^6\d{2}1\d{2}$")


def generate_device_number() -> int:
	"""Генерує випадковий номер пристрою у форматі 6xx1xx."""

	return int(
		f"6"
		f"{random.randint(0, 9)}"
		f"{random.randint(0, 9)}"
		f"1"
		f"{random.randint(0, 9)}"
		f"{random.randint(0, 9)}"
	)


def generate_unique_device_numbers(count: int) -> list[int]:
	"""Генерує список унікальних номерів пристроїв."""

	if count < 0:
		raise ValueError("count must be non-negative")

	numbers: set[int] = set()
	while len(numbers) < count:
		numbers.add(generate_device_number())
	return list(numbers)


@dataclass(frozen=True)
class HashTableItem:
	key: int
	value: str | None = None


class ClosedHashTable:
	"""Хеш-таблиця із закритим хешуванням та лінійним зондуванням."""

	_DELETED = object()

	def __init__(self, capacity: int = 17) -> None:
		if capacity <= 0:
			raise ValueError("capacity must be positive")
		self._capacity = capacity
		self._table: list[HashTableItem | object | None] = [None] * capacity
		self._size = 0

	@staticmethod
	def validate_device_number(key: int) -> bool:
		"""Перевіряє, чи відповідає число формату 6xx1xx."""

		return bool(DEVICE_NUMBER_PATTERN.fullmatch(str(key)))

	def _hash(self, key: int) -> int:
		return key % self._capacity

	def _find_slot(self, key: int) -> int:
		"""Повертає індекс для вставки або пошуку елемента."""

		start_index = self._hash(key)
		first_deleted_index: int | None = None

		for step in range(self._capacity):
			index = (start_index + step) % self._capacity
			slot = self._table[index]

			if slot is None:
				return first_deleted_index if first_deleted_index is not None else index

			if slot is self._DELETED:
				if first_deleted_index is None:
					first_deleted_index = index
				continue

			if isinstance(slot, HashTableItem) and slot.key == key:
				return index

		if first_deleted_index is not None:
			return first_deleted_index

		raise OverflowError("Hash table is full")

	def insert(self, key: int, value: str | None = None) -> bool:
		"""Додає елемент у таблицю. Повертає False, якщо ключ уже існує."""

		if not self.validate_device_number(key):
			raise ValueError("Device number must match format 6xx1xx")

		index = self._find_slot(key)
		slot = self._table[index]

		if isinstance(slot, HashTableItem) and slot.key == key:
			return False

		self._table[index] = HashTableItem(key=key, value=value)
		self._size += 1
		return True

	def search(self, key: int) -> int:
		"""Повертає індекс елемента або -1, якщо ключ не знайдено."""

		if not self.validate_device_number(key):
			return -1

		start_index = self._hash(key)

		for step in range(self._capacity):
			index = (start_index + step) % self._capacity
			slot = self._table[index]

			if slot is None:
				return -1

			if slot is self._DELETED:
				continue

			if isinstance(slot, HashTableItem) and slot.key == key:
				return index

		return -1

	def delete(self, key: int) -> bool:
		"""Видаляє елемент з таблиці."""

		index = self.search(key)
		if index == -1:
			return False

		self._table[index] = self._DELETED
		self._size -= 1
		return True

	def get(self, key: int) -> HashTableItem | None:
		index = self.search(key)
		if index == -1:
			return None

		slot = self._table[index]
		return slot if isinstance(slot, HashTableItem) else None

	@property
	def size(self) -> int:
		return self._size

	@property
	def capacity(self) -> int:
		return self._capacity

	def load_factor(self) -> float:
		return self._size / self._capacity

	def items(self) -> list[HashTableItem]:
		return [slot for slot in self._table if isinstance(slot, HashTableItem)]

	def __str__(self) -> str:
		rows: list[str] = []
		for index, slot in enumerate(self._table):
			if slot is None:
				rows.append(f"{index:>2}: EMPTY")
			elif slot is self._DELETED:
				rows.append(f"{index:>2}: DELETED")
			else:
				rows.append(f"{index:>2}: {slot.key}")
		return "\n".join(rows)


def build_demo_table() -> ClosedHashTable:
	"""Створює демонстраційну таблицю з кількома пристроями."""

	table = ClosedHashTable(capacity=17)
	for number in generate_unique_device_numbers(10):
		table.insert(number)
	return table


if __name__ == "__main__":
	def _find_device_numbers_with_mod(mod: int, count: int, size: int) -> list[int]:
		"""Повертає `count` номерів формату 6xx1xx, що дають залишок `mod` при діленні на `size`."""
		results: list[int] = []
		n = 600000
		while len(results) < count and n <= 699999:
			s = str(n)
			if DEVICE_NUMBER_PATTERN.fullmatch(s) and int(s) % size == mod:
				results.append(int(s))
			n += 1
		if len(results) < count:
			raise ValueError("Не вдалося знайти достатньо номерів для заданих параметрів")
		return results

	def _simulate_insert_and_count_probes(table: ClosedHashTable, key: int) -> int:
		"""Імітує вставку (лінійне зондування) і повертає кількість проб (probes).
		Безпечна операція: використовує внутрішні структури таблиці.
		"""
		if not table.validate_device_number(key):
			raise ValueError("Invalid device number format")

		start = table._hash(key)
		for step in range(table._capacity):
			idx = (start + step) % table._capacity
			slot = table._table[idx]
			if slot is None or slot is table._DELETED:
				table._table[idx] = HashTableItem(key=key)
				table._size += 1
				return step + 1
			if isinstance(slot, HashTableItem) and slot.key == key:
				return 0
		raise OverflowError("Table full")

	def _simulate_search_probes(table: ClosedHashTable, key: int) -> int:
		if not table.validate_device_number(key):
			return 0
		start = table._hash(key)
		for step in range(table._capacity):
			idx = (start + step) % table._capacity
			slot = table._table[idx]
			if slot is None:
				return 0
			if slot is table._DELETED:
				continue
			if isinstance(slot, HashTableItem) and slot.key == key:
				return step + 1
		return 0

	def run_detailed_tests():
		print("== Детальні тести для хеш-таблиці (закрите хешування, лінійне зондування) ==\n")

		# Параметри для тестів
		capacity = 11
		n = 6

		# Best-case: вибираємо числа з різними залишками modulo capacity
		best_table = ClosedHashTable(capacity=capacity)
		best_numbers: list[int] = []
		for mod in range(n):
			best_numbers.extend(_find_device_numbers_with_mod(mod, 1, capacity))

		best_probes = 0
		for num in best_numbers:
			probes = _simulate_insert_and_count_probes(best_table, num)
			best_probes += probes

		print("Best-case scenario (без колізій)")
		print(f"Вставлено {len(best_numbers)} елементів у таблицю місткістю {capacity}")
		print(f"Сумарна кількість проб: {best_probes}")
		print(f"Середня кількість проб на вставку: {best_probes/len(best_numbers):.2f}\n")

		# Worst-case: підбираємо числа з однаковим залишком (всі колізії йдуть в один ланцюжок)
		worst_table = ClosedHashTable(capacity=capacity)
		# вибираємо один модуль
		collision_mod = 0
		worst_numbers = _find_device_numbers_with_mod(collision_mod, n, capacity)

		worst_probes = 0
		for num in worst_numbers:
			probes = _simulate_insert_and_count_probes(worst_table, num)
			worst_probes += probes

		print("Worst-case scenario (максимальні колізії)")
		print(f"Вставлено {len(worst_numbers)} елементів у таблицю місткістю {capacity}")
		print(f"Сумарна кількість проб: {worst_probes}")
		print(f"Середня кількість проб на вставку: {worst_probes/len(worst_numbers):.2f}\n")

		# Перевірка пошуку: вимірюємо кількість проб для кожного знайденого ключа
		print("Проби при пошуку (worst-case):")
		for num in worst_numbers:
			probes = _simulate_search_probes(worst_table, num)
			print(f"{num} -> probes={probes}")

		# Перевірка видалення і повторного вставлення
		print("\nПеревірка видалення і повторного використання DELETED слота:")
		to_delete = worst_numbers[2]
		print(f"Видаляємо {to_delete} -> success={worst_table.delete(to_delete)}")
		# вставляємо новий номер з тим же модулем
		new_num = _find_device_numbers_with_mod(collision_mod, 1, capacity)[0]
		probes_new = _simulate_insert_and_count_probes(worst_table, new_num)
		print(f"Вставляємо новий {new_num} -> probes={probes_new}")

		print("\nПоточний стан worst_table:")
		print(worst_table)

	# Запускаємо тести
	run_detailed_tests()
