"""Лабораторна робота: алгоритми хешування (4 завдання).

Вимоги реалізовано у процедурному стилі:
1) Хеш-таблиця літер і їх кількостей у рядку.
2) Хеш-таблиця слів із текстового файлу з підрахунком порівнянь.
3) Хеш-таблиця зарезервованих слів мови програмування з HELP.
4) Хеш-таблиця цілих чисел із файлу та порівняння порівнянь для різних наборів.

Усі результати дублюються на екран і у вихідний файл.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


OUTPUT_FILE = "lab7_output.txt"
WORD_PATTERN = re.compile(r"[A-Za-zА-Яа-яІіЇїЄєҐґ']+")


class Reporter:
    """Дублює виведення: консоль + файл."""

    def __init__(self, path: str) -> None:
        self.path = path
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("=== Звіт лабораторної роботи з хешування ===\n")

    def log(self, text: str = "") -> None:
        print(text)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(text + "\n")


@dataclass
class SearchResult:
    """Результат пошуку із підрахунком порівнянь."""

    found: bool
    value: object | None
    comparisons: int


class ChainingHashTable:
    """Хеш-таблиця з методом ланцюжків (separate chaining)."""

    def __init__(self, size: int) -> None:
        if size <= 0:
            raise ValueError("Розмір таблиці має бути додатним")
        self.size = size
        self.buckets: list[list[tuple[object, object]]] = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key: object) -> int:
        return hash(key) % self.size

    def load_factor(self) -> float:
        return self.count / self.size

    def insert(self, key: object, value: object) -> int:
        """Вставляє або оновлює ключ. Повертає кількість порівнянь."""

        idx = self._hash(key)
        bucket = self.buckets[idx]
        comparisons = 0

        for i, (k, _) in enumerate(bucket):
            comparisons += 1
            if k == key:
                bucket[i] = (key, value)
                return comparisons

        bucket.append((key, value))
        self.count += 1
        return comparisons + 1

    def search(self, key: object) -> SearchResult:
        """Пошук ключа з підрахунком порівнянь."""

        idx = self._hash(key)
        bucket = self.buckets[idx]
        comparisons = 0

        for k, v in bucket:
            comparisons += 1
            if k == key:
                return SearchResult(True, v, comparisons)

        return SearchResult(False, None, comparisons)

    def delete_keys_startswith(self, letter: str) -> int:
        """Видаляє рядкові ключі, що починаються на вказану літеру."""

        removed = 0
        low = letter.lower()

        for idx in range(self.size):
            old_bucket = self.buckets[idx]
            new_bucket: list[tuple[object, object]] = []
            for k, v in old_bucket:
                if isinstance(k, str) and k.lower().startswith(low):
                    removed += 1
                    self.count -= 1
                else:
                    new_bucket.append((k, v))
            self.buckets[idx] = new_bucket

        return removed

    def items(self) -> list[tuple[object, object]]:
        all_items: list[tuple[object, object]] = []
        for bucket in self.buckets:
            all_items.extend(bucket)
        return all_items


def print_hash_table(table: ChainingHashTable, title: str, reporter: Reporter) -> None:
    """Друк таблиці по кошиках."""

    reporter.log(title)
    for i, bucket in enumerate(table.buckets):
        if not bucket:
            reporter.log(f"[{i:>3}] -> []")
        else:
            parts = [f"{k}:{v}" for k, v in bucket]
            reporter.log(f"[{i:>3}] -> " + " | ".join(parts))
    reporter.log(f"Елементів: {table.count}, load factor: {table.load_factor():.3f}")
    reporter.log("-" * 72)


def read_int(prompt: str, min_value: int | None = None) -> int:
    """Безпечне читання цілого числа з консолі."""

    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if min_value is not None and value < min_value:
                print(f"Введіть число >= {min_value}")
                continue
            return value
        except ValueError:
            print("Помилка: введіть ціле число")


def read_non_empty(prompt: str) -> str:
    """Читає непорожній рядок."""

    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Помилка: рядок не може бути порожнім")


def task1_letters_count(reporter: Reporter) -> None:
    """Завдання 1: хеш-таблиця літер і кількості входжень."""

    reporter.log("\nЗАВДАННЯ 1: ЛІТЕРИ У РЯДКУ")
    text = read_non_empty("Введіть рядок: ")

    size = max(11, len(text) * 2 + 1)
    table = ChainingHashTable(size)

    for ch in text:
        if ch.isalpha():
            key = ch.lower()
            existing = table.search(key)
            if existing.found:
                table.insert(key, int(existing.value) + 1)
            else:
                table.insert(key, 1)

    print_hash_table(table, "Хеш-таблиця літер (літера:кількість):", reporter)

    letter = read_non_empty("Введіть літеру для пошуку: ")[0].lower()
    result = table.search(letter)
    if result.found:
        reporter.log(
            f"Літеру '{letter}' знайдено, кількість: {result.value}, порівнянь: {result.comparisons}"
        )
    else:
        reporter.log(
            f"Літеру '{letter}' не знайдено, порівнянь під час пошуку: {result.comparisons}"
        )


def extract_words(text: str) -> list[str]:
    """Виділяє слова та нормалізує до нижнього регістру."""

    return [w.lower() for w in WORD_PATTERN.findall(text)]


def build_word_table(words: Iterable[str], size: int) -> ChainingHashTable:
    """Створює хеш-таблицю слів, де value = кількість входжень слова."""

    table = ChainingHashTable(size)
    for word in words:
        existing = table.search(word)
        if existing.found:
            table.insert(word, int(existing.value) + 1)
        else:
            table.insert(word, 1)
    return table


def task2_words_file(reporter: Reporter) -> None:
    """Завдання 2: хеш-таблиця слів з текстового файлу."""

    reporter.log("\nЗАВДАННЯ 2: СЛОВА ІЗ ТЕКСТОВОГО ФАЙЛУ")
    path = read_non_empty("Введіть шлях до текстового файлу: ")
    size = read_int("Введіть розмірність хеш-таблиці: ", min_value=1)

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    words = extract_words(text)
    if not words:
        reporter.log("У файлі не знайдено слів.")
        return

    table = build_word_table(words, size)
    print_hash_table(table, "Побудована таблиця слів (слово:кількість):", reporter)

    query = read_non_empty("Введіть слово для пошуку: ").lower()
    result = table.search(query)
    if result.found:
        reporter.log(
            f"Слово '{query}' знайдено, кількість: {result.value}, порівнянь: {result.comparisons}"
        )
    else:
        reporter.log(f"Слово '{query}' не знайдено, порівнянь: {result.comparisons}")

    reporter.log("Порівняння кількості порівнянь для різних розмірностей таблиці:")
    base_sizes = sorted({max(5, size // 2), size, size * 2})
    for s in base_sizes:
        t = build_word_table(words, s)
        r = t.search(query)
        reporter.log(
            f"size={s:>5}: found={r.found}, comparisons={r.comparisons}, load={t.load_factor():.3f}"
        )

    first_letter = read_non_empty("Введіть літеру для видалення слів (початкова): ")[0]
    removed = table.delete_keys_startswith(first_letter)
    reporter.log(f"Видалено слів, що починаються на '{first_letter}': {removed}")
    print_hash_table(table, "Таблиця після видалення:", reporter)


def default_reserved_help() -> dict[str, str]:
    """Базовий набір резервованих слів Python (20+)."""

    return {
        "if": "Умовний оператор.",
        "else": "Альтернативна гілка умовного оператора.",
        "elif": "Додаткова умова у ланцюжку if.",
        "for": "Цикл з ітерацією по послідовності.",
        "while": "Цикл із передумовою.",
        "break": "Перериває поточний цикл.",
        "continue": "Переходить до наступної ітерації циклу.",
        "def": "Оголошення функції.",
        "return": "Повертає значення з функції.",
        "class": "Оголошення класу.",
        "try": "Початок блоку обробки винятків.",
        "except": "Гілка обробки винятку.",
        "finally": "Блок, що виконується завжди після try.",
        "raise": "Явно генерує виняток.",
        "import": "Імпортує модуль.",
        "from": "Імпортує об'єкти з модуля.",
        "as": "Псевдонім при імпорті або у with.",
        "with": "Контекстний менеджер ресурсів.",
        "pass": "Порожня інструкція (нічого не робить).",
        "lambda": "Анонімна функція.",
        "global": "Оголошення глобальної змінної у функції.",
        "nonlocal": "Оголошення змінної зовнішньої (не глобальної) області.",
    }


def rehash_table(old_table: ChainingHashTable, new_size: int) -> tuple[ChainingHashTable, int]:
    """Реструктуризація: перенос елементів у нову таблицю більшого розміру."""

    new_table = ChainingHashTable(new_size)
    total_comparisons = 0
    for k, v in old_table.items():
        total_comparisons += new_table.insert(k, v)
    return new_table, total_comparisons


def insert_with_optional_rehash(
    table: ChainingHashTable,
    key: str,
    value: str,
    threshold: float = 0.75,
) -> tuple[ChainingHashTable, int, bool]:
    """Вставка з авто-реорганізацією таблиці при високому заповненні."""

    comparisons = 0
    rehashed = False
    if table.load_factor() >= threshold:
        table, c = rehash_table(table, table.size * 2 + 1)
        comparisons += c
        rehashed = True
    comparisons += table.insert(key, value)
    return table, comparisons, rehashed


def evaluate_insert_efficiency(base_data: dict[str, str], reporter: Reporter) -> None:
    """Порівнює ефективність вставки/реструктуризації при різному заповненні."""

    reporter.log("Порівняння ефективності додавання ключа (різна степінь заповненості):")
    probes = [0.40, 0.70, 0.90]

    for target_load in probes:
        cap = 23
        table = ChainingHashTable(cap)
        data_items = list(base_data.items())
        idx = 0

        while table.load_factor() < target_load and idx < len(data_items):
            k, v = data_items[idx]
            table.insert(k, v)
            idx += 1

        new_key = f"new_kw_{int(target_load * 100)}"
        new_help = "Додане користувачем слово."  # тестове значення
        table_after, comps, rehashed = insert_with_optional_rehash(table, new_key, new_help)

        reporter.log(
            f"load_before~{target_load:.2f}, real={table.load_factor():.3f}, "
            f"comparisons={comps}, rehash={rehashed}, new_size={table_after.size}"
        )


def task3_reserved_help(reporter: Reporter) -> None:
    """Завдання 3: HELP по зарезервованих словах і додавання нового ключа."""

    reporter.log("\nЗАВДАННЯ 3: ЗАРЕЗЕРВОВАНІ СЛОВА + HELP")
    base_help = default_reserved_help()

    table = ChainingHashTable(31)
    for k, v in base_help.items():
        table.insert(k, v)

    print_hash_table(table, "Хеш-таблиця зарезервованих слів (слово:HELP):", reporter)

    word = read_non_empty("Введіть зарезервоване слово для підказки: ").lower()
    result = table.search(word)
    if result.found:
        reporter.log(f"HELP[{word}] = {result.value}")
        reporter.log(f"Порівнянь під час пошуку: {result.comparisons}")
    else:
        reporter.log(f"Слово '{word}' не знайдено")

    add_word = read_non_empty("Введіть нове слово для додавання: ").lower()
    add_help = read_non_empty("Введіть HELP для нового слова: ")

    table, comps, rehashed = insert_with_optional_rehash(table, add_word, add_help, threshold=0.75)
    reporter.log(
        f"Нове слово '{add_word}' додано. comparisons={comps}, rehash={rehashed}, size={table.size}"
    )

    evaluate_insert_efficiency(base_help, reporter)
    print_hash_table(table, "Оновлена таблиця зарезервованих слів:", reporter)


def parse_integer_sets_from_file(path: str) -> list[list[int]]:
    """Зчитує набори чисел: кожен рядок файлу - окремий набір.

    Якщо у файлі лише один рядок, ділить його на 3 частини для порівняння.
    """

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    sets: list[list[int]] = []
    for line in lines:
        nums = [int(x) for x in re.findall(r"-?\d+", line)]
        if nums:
            sets.append(nums)

    if not sets:
        return []

    if len(sets) == 1:
        arr = sets[0]
        if len(arr) < 3:
            return [arr]
        third = max(1, len(arr) // 3)
        return [arr[:third], arr[third : 2 * third], arr[2 * third :]]

    return sets


def build_int_table(nums: Iterable[int], size: int) -> ChainingHashTable:
    """Будує таблицю цілих чисел; value - кількість входжень."""

    table = ChainingHashTable(size)
    for n in nums:
        existing = table.search(n)
        if existing.found:
            table.insert(n, int(existing.value) + 1)
        else:
            table.insert(n, 1)
    return table


def task4_integers_file(reporter: Reporter) -> None:
    """Завдання 4: хеш-таблиця цілих чисел із файлу, пошук і порівняння."""

    reporter.log("\nЗАВДАННЯ 4: ЦІЛІ ЧИСЛА ІЗ ФАЙЛУ")
    path = read_non_empty("Введіть шлях до файлу з цілими числами: ")
    sets = parse_integer_sets_from_file(path)

    if not sets:
        reporter.log("У файлі не знайдено числових даних.")
        return

    query = read_int("Введіть ціле число для пошуку: ")

    reporter.log("Порівняння результатів пошуку для різних наборів даних:")
    for i, data_set in enumerate(sets, start=1):
        size = max(11, len(data_set) * 2 + 1)
        table = build_int_table(data_set, size)
        result = table.search(query)
        reporter.log(
            f"Набір #{i}: n={len(data_set)}, size={size}, "
            f"found={result.found}, count={result.value if result.found else 0}, "
            f"comparisons={result.comparisons}, load={table.load_factor():.3f}"
        )


def print_menu(reporter: Reporter) -> None:
    """Головне меню запуску завдань."""

    reporter.log("\nОберіть дію:")
    reporter.log("1 - Завдання 1 (літери у рядку)")
    reporter.log("2 - Завдання 2 (слова з файлу)")
    reporter.log("3 - Завдання 3 (зарезервовані слова + HELP)")
    reporter.log("4 - Завдання 4 (цілі числа з файлу)")
    reporter.log("5 - Виконати всі завдання послідовно")
    reporter.log("0 - Вихід")


def run() -> None:
    """Точка входу програми."""

    reporter = Reporter(OUTPUT_FILE)
    reporter.log("Лабораторна робота: Хеш-таблиці")
    reporter.log(f"Вихідний файл: {OUTPUT_FILE}")

    while True:
        print_menu(reporter)
        choice = read_non_empty("Ваш вибір: ")

        if choice == "1":
            task1_letters_count(reporter)
        elif choice == "2":
            task2_words_file(reporter)
        elif choice == "3":
            task3_reserved_help(reporter)
        elif choice == "4":
            task4_integers_file(reporter)
        elif choice == "5":
            task1_letters_count(reporter)
            task2_words_file(reporter)
            task3_reserved_help(reporter)
            task4_integers_file(reporter)
        elif choice == "0":
            reporter.log("Завершення програми.")
            break
        else:
            reporter.log("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    run()
