import re
import os
from typing import List, Tuple


class HashTable:
    """
    Реалізація хеш-таблиці з методом ланцюжків для обробки колізій
    """
    
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.comparisons = 0
        self.total_comparisons = 0
    
    def hash_function(self, key):
        """
        Хеш-функція: сума ASCII кодів символів за модулем розмірності
        """
        return sum(ord(c) for c in key) % self.size
    
    def insert(self, key, value=1):
        """
        Вставлення елемента в таблицю
        """
        index = self.hash_function(key)
        bucket = self.table[index]
        
        # Перевірка, чи слово вже існує
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value + v)
                return
        
        bucket.append((key, value))
    
    def search(self, key) -> Tuple[bool, int]:
        """
        Пошук слова в таблиці
        :return: (знайдено, кількість порівнянь)
        """
        self.comparisons = 0
        index = self.hash_function(key)
        bucket = self.table[index]
        
        for k, v in bucket:
            self.comparisons += 1
            if k == key:
                return True, v, self.comparisons
        
        return False, 0, self.comparisons
    
    def delete_by_letter(self, letter):
        """
        Видалення всіх слів, які починаються на вказану букву
        :return: кількість видалених слів
        """
        deleted_count = 0
        
        for bucket in self.table:
            items_to_remove = []
            for k, v in bucket:
                if k.lower().startswith(letter.lower()):
                    items_to_remove.append((k, v))
                    deleted_count += 1
            
            for item in items_to_remove:
                bucket.remove(item)
        
        return deleted_count
    
    def display(self):
        """
        Вивід таблиці на екран
        """
        print("\n" + "="*70)
        print(f"ХЕШ-ТАБЛИЦЯ (Розмір: {self.size})")
        print("="*70)
        
        word_count = 0
        for i, bucket in enumerate(self.table):
            if bucket:
                print(f"\n[Індекс {i:3}]")
                for word, count in bucket:
                    print(f"  → {word:20} : {count:>4} входжень")
                    word_count += 1
        
        if word_count == 0:
            print("Таблиця пуста!")
        else:
            print(f"\n{'='*70}")
            print(f"Всього унікальних слів: {word_count}")
            print(f"{'='*70}\n")
    
    def get_statistics(self):
        """
        Отримати статистику таблиці
        """
        bucket_sizes = [len(bucket) for bucket in self.table]
        non_empty = sum(1 for b in bucket_sizes if b > 0)
        max_collision = max(bucket_sizes) if bucket_sizes else 0
        avg_collision = sum(bucket_sizes) / non_empty if non_empty > 0 else 0
        
        return {
            'size': self.size,
            'non_empty_buckets': non_empty,
            'max_collision_chain': max_collision,
            'avg_collision_chain': avg_collision,
            'total_words': sum(bucket_sizes)
        }


def read_file(filename):
    """
    Читання слів з файлу
    """
    words = []
    
    if not os.path.exists(filename):
        print(f"❌ Файл '{filename}' не знайдено!")
        return words
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
            # Видалення пунктуації та розділення на слова
            words = re.findall(r'\b[a-zA-Z]+\b', text)
    except Exception as e:
        print(f"❌ Помилка при читанні файлу: {e}")
    
    return words


def main():
    print("\n" + "="*70)
    print("ПРОГРАМА: ХЕШ-ТАБЛИЦЯ ЗІ СЛІВ ТЕКСТОВОГО ФАЙЛУ")
    print("="*70 + "\n")
    
    # Вибір файлу
    filename = input("Введіть назву файлу: ").strip()
    
    # Читання слів
    words = read_file(filename)
    
    if not words:
        print("❌ Не вдалося прочитати слова з файлу!")
        return
    
    print(f"✓ Прочитано {len(words)} слів\n")
    
    # Отримання розмірності таблиці
    while True:
        try:
            table_size = int(input("Введіть розмірність хеш-таблиці: "))
            if table_size <= 0:
                print("❌ Розмірність повинна бути позитивною!\n")
                continue
            break
        except ValueError:
            print("❌ Будь ласка, введіть ціле число!\n")
    
    # Створення хеш-таблиці
    hash_table = HashTable(table_size)
    
    # Вставлення слів
    print(f"\n⏳ Побудова таблиці...")
    for word in words:
        hash_table.insert(word.lower())
    print("✓ Таблиця побудована!\n")
    
    # Вивід статистики
    stats = hash_table.get_statistics()
    print("СТАТИСТИКА ТАБЛИЦІ:")
    print(f"  Розмір таблиці: {stats['size']}")
    print(f"  Всього слів: {stats['total_words']}")
    print(f"  Занятих клітинок: {stats['non_empty_buckets']}")
    print(f"  Макс. довжина ланцюжка: {stats['max_collision_chain']}")
    print(f"  Середня довжина ланцюжка: {stats['avg_collision_chain']:.2f}\n")
    
    # Пошук слів
    while True:
        search_word = input("Введіть слово для пошуку (або 'кінець' для завершення): ").strip().lower()
        
        if search_word == 'кінець':
            break
        
        if not search_word:
            print("❌ Будь ласка, введіть слово!\n")
            continue
        
        found, count, comparisons = hash_table.search(search_word)
        
        if found:
            print(f"✓ Слово '{search_word}' знайдено!")
            print(f"  Входжень: {count}")
            print(f"  Порівнянь здійснено: {comparisons}\n")
        else:
            print(f"❌ Слово '{search_word}' не знайдено!")
            print(f"  Порівнянь здійснено: {comparisons}\n")
    
    # Видалення слів за буквою
    while True:
        delete_letter = input("\nВведіть букву для видалення всіх слів, що починаються з неї (або 'кінець'): ").strip().lower()
        
        if delete_letter == 'кінець':
            break
        
        if len(delete_letter) != 1 or not delete_letter.isalpha():
            print("❌ Будь ласка, введіть одну букву!\n")
            continue
        
        deleted = hash_table.delete_by_letter(delete_letter)
        print(f"✓ Видалено {deleted} слів, що починаються на '{delete_letter}'\n")
        
        # Оновлена статистика
        stats = hash_table.get_statistics()
        print("ОНОВЛЕНА СТАТИСТИКА:")
        print(f"  Всього слів: {stats['total_words']}")
        print(f"  Занятих клітинок: {stats['non_empty_buckets']}\n")


def compare_different_sizes():
    """
    Порівняння кількості порівнянь для різних розмірностей таблиці
    """
    print("\n" + "="*70)
    print("ПОРІВНЯННЯ КІЛЬКОСТІ ПОРІВНЯНЬ ДЛЯ РІЗНИХ РОЗМІРНОСТЕЙ")
    print("="*70 + "\n")
    
    filename = input("Введіть назву файлу для аналізу: ").strip()

    
    words = read_file(filename)
    
    if not words:
        return
    
    search_word = input("Введіть слово для тестування пошуку: ").strip().lower()
    
    print(f"\n{'Розмір':<10} {'Занято':<10} {'Макс. ланц.':<15} {'Пошуків':<10} {'Порівняння':<12}")
    print("-" * 70)
    
    sizes = [200, 300, 500, 700, 1000, 1300]
    
    for size in sizes:
        hash_table = HashTable(size)
        
        for word in words:
            hash_table.insert(word.lower())
        
        found, count, comparisons = hash_table.search(search_word)
        stats = hash_table.get_statistics()
        
        status = "✓" if found else "✗"
        print(f"{size:<10} {stats['non_empty_buckets']:<10} {stats['max_collision_chain']:<15} {status:<10} {comparisons:<12}")
    
    print("\n")


if __name__ == "__main__":
    while True:
        print("\nВИБІР РЕЖИМУ РОБОТИ:")
        print("1. Побудувати хеш-таблицю та працювати з нею")
        print("2. Порівняти різні розмірності таблиці")
        print("3. Вихід")
        
        choice = input("\nВиберіть режим (1-3): ").strip()
        
        if choice == '1':
            main()
        elif choice == '2':
            compare_different_sizes()
        elif choice == '3':
            print("\nДо побачення!")
            break
        else:
            print("❌ Невірний вибір!")
