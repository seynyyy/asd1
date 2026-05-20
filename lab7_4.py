import random
import time
import os
from typing import Tuple, List, Dict


class IntegerHashTable:
    """
    Реалізація хеш-таблиці для цілих чисел з методом ланцюжків
    """
    
    def __init__(self, size=53):
        """
        Ініціалізація хеш-таблиці
        :param size: розмірність таблиці
        """
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0
        self.comparisons = 0
    
    def hash_function(self, key):
        """
        Хеш-функція для цілих чисел: модульна арифметика
        """
        return abs(key) % self.size
    
    def insert(self, key):
        """
        Вставлення числа в таблицю
        :return: True якщо вставлено, False якщо вже існувало
        """
        index = self.hash_function(key)
        bucket = self.table[index]
        
        # Перевірка, чи число вже існує
        for num in bucket:
            if num == key:
                return False
        
        bucket.append(key)
        self.count += 1
        return True
    
    def search(self, key) -> Tuple[bool, int]:
        """
        Пошук числа в таблиці
        :return: (знайдено, кількість порівнянь)
        """
        self.comparisons = 0
        index = self.hash_function(key)
        bucket = self.table[index]
        
        for num in bucket:
            self.comparisons += 1
            if num == key:
                return True, self.comparisons
        
        return False, self.comparisons
    
    def delete(self, key) -> bool:
        """
        Видалення числа з таблиці
        """
        index = self.hash_function(key)
        bucket = self.table[index]
        
        for i, num in enumerate(bucket):
            if num == key:
                bucket.pop(i)
                self.count -= 1
                return True
        
        return False
    
    def display(self):
        """
        Вивід таблиці на екран
        """
        print("\n" + "="*70)
        print(f"ХЕШ-ТАБЛИЦЯ ЦІЛИХ ЧИСЕЛ (Розмір: {self.size})")
        print("="*70)
        
        word_count = 0
        for i, bucket in enumerate(self.table):
            if bucket:
                print(f"\n[Індекс {i:3}] ({len(bucket)} числ(а/о)):")
                sorted_bucket = sorted(bucket)
                print(f"  {sorted_bucket}")
                word_count += len(bucket)
        
        if word_count == 0:
            print("Таблиця пуста!")
        else:
            print(f"\n{'='*70}")
            print(f"Всього унікальних чисел: {word_count}")
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
            'count': self.count,
            'non_empty_buckets': non_empty,
            'max_collision_chain': max_collision,
            'avg_collision_chain': avg_collision,
            'load_factor': self.count / self.size
        }


def generate_test_file(filename, count, data_type='random'):
    """
    Генерування тестового файлу з цілими числами
    :param filename: ім'я файлу
    :param count: кількість чисел
    :param data_type: тип даних - 'random', 'sorted', 'reverse', 'duplicates', 'clustered'
    """
    print(f"Генерування файлу '{filename}' ({data_type}, {count} чисел)...", end=" ")
    
    numbers = []
    
    if data_type == 'random':
        numbers = [random.randint(1, 10000) for _ in range(count)]
    
    elif data_type == 'sorted':
        numbers = list(range(1, count + 1))
    
    elif data_type == 'reverse':
        numbers = list(range(count, 0, -1))
    
    elif data_type == 'duplicates':
        # Багато дублікатів
        unique_numbers = random.sample(range(1, 100), min(10, count))
        numbers = [random.choice(unique_numbers) for _ in range(count)]
    
    elif data_type == 'clustered':
        # Числа сконцентровані в певних діапазонах
        cluster_ranges = [(1, 100), (1000, 1100), (5000, 5100), (9900, 10000)]
        numbers = []
        per_cluster = count // len(cluster_ranges)
        for start, end in cluster_ranges:
            numbers.extend([random.randint(start, end) for _ in range(per_cluster)])
        random.shuffle(numbers)
        numbers = numbers[:count]
    
    with open(filename, 'w') as f:
        f.write(' '.join(map(str, numbers)))
    
    print("✓")
    return filename


def read_numbers_from_file(filename):
    """
    Читання цілих чисел з файлу
    """
    if not os.path.exists(filename):
        print(f"❌ Файл '{filename}' не знайдено!")
        return []
    
    try:
        with open(filename, 'r') as f:
            text = f.read()
            numbers = list(map(int, text.split()))
        return numbers
    except Exception as e:
        print(f"❌ Помилка при читанні файлу: {e}")
        return []


def create_sample_file():
    """
    Створення прикладу файлу з числами
    """
    sample_numbers =  [random.randint(1, 1000) for _ in range(5000)]
    
    with open('numbers.txt', 'w') as f:
        f.write(' '.join(map(str, sample_numbers)))
    
    return 'numbers.txt'


def main():
    """
    Основна функція програми
    """
    print("\n" + "="*70)
    print("ПРОГРАМА: ХЕШ-ТАБЛИЦЯ ЦІЛИХ ЧИСЕЛ ІЗ ФАЙЛУ")
    print("="*70 + "\n")
    
    # Вибір файлу
    filename = input("Введіть назву файлу (або натисніть Enter для створення прикладу): ").strip()
    
    if not filename:
        filename = create_sample_file()
        print(f"✓ Створено файл прикладу: {filename}\n")
    
    # Читання чисел
    numbers = read_numbers_from_file(filename)
    
    if not numbers:
        print("❌ Не вдалося прочитати числа з файлу!")
        return
    
    print(f"✓ Прочитано {len(numbers)} чисел")
    unique_numbers = len(set(numbers))
    print(f"  Унікальних чисел: {unique_numbers}")
    print(f"  Діапазон: [{min(numbers)}, {max(numbers)}]\n")
    
    # Отримання розмірності таблиці
    while True:
        try:
            table_size = int(input("Введіть розмірність хеш-таблиці (рекомендується: 20-100): "))
            if table_size <= 0:
                print("❌ Розмірність повинна бути позитивною!\n")
                continue
            break
        except ValueError:
            print("❌ Будь ласка, введіть ціле число!\n")
    
    # Створення хеш-таблиці
    hash_table = IntegerHashTable(table_size)
    
    # Вставлення чисел
    print(f"\n⏳ Побудова таблиці...")
    inserted = 0
    for num in numbers:
        if hash_table.insert(num):
            inserted += 1
    print(f"✓ Таблиця побудована!")
    print(f"  Вставлено унікальних чисел: {inserted}\n")
    
    # Вивід таблиці
    hash_table.display()
    
    # Вивід статистики
    stats = hash_table.get_statistics()
    print("СТАТИСТИКА ТАБЛИЦІ:")
    print(f"  Розмір таблиці: {stats['size']}")
    print(f"  Унікальних чисел: {stats['count']}")
    print(f"  Занятих клітинок: {stats['non_empty_buckets']}")
    print(f"  Макс. довжина ланцюжка: {stats['max_collision_chain']}")
    print(f"  Середня довжина ланцюжка: {stats['avg_collision_chain']:.2f}")
    print(f"  Коефіцієнт наповненості: {stats['load_factor']:.2%}\n")
    
    # Пошук чисел
    while True:
        try:
            search_num = input("Введіть число для пошуку (або 'кінець' для завершення): ").strip().lower()
            
            if search_num == 'кінець':
                break
            
            num = int(search_num)
            found, comparisons = hash_table.search(num)
            
            if found:
                print(f"✓ Число {num} знайдено!")
                print(f"  Порівнянь здійснено: {comparisons}\n")
            else:
                print(f"❌ Число {num} не знайдено!")
                print(f"  Порівнянь здійснено: {comparisons}\n")
        
        except ValueError:
            print("❌ Будь ласка, введіть ціле число!\n")


def compare_datasets():
    """
    Порівняння результатів для різних наборів даних
    """
    print("\n" + "="*70)
    print("ПОРІВНЯННЯ РЕЗУЛЬТАТІВ ДЛЯ РІЗНИХ НАБОРІВ ДАНИХ")
    print("="*70 + "\n")
    
    dataset_count = 1000
    table_size = 53
    
    datasets = {
        'Випадкові числа': 'random',
        'Відсортовані числа': 'sorted',
        'Числа в зворотному порядку': 'reverse',
        'З багатьма дублікатами': 'duplicates',
        'Скупчені числа': 'clustered'
    }
    
    results = []
    
    print(f"Параметри тестування:")
    print(f"  Кількість чисел: {dataset_count}")
    print(f"  Розмір таблиці: {table_size}")
    print(f"  Тестування на {dataset_count // 10} пошуків\n")
    print("-" * 70)
    
    for dataset_name, data_type in datasets.items():
        print(f"\n📊 {dataset_name}:")
        
        # Генерування та завантаження файлу
        filename = f"test_{data_type}.txt"
        generate_test_file(filename, dataset_count, data_type)
        numbers = read_numbers_from_file(filename)
        
        # Створення таблиці
        hash_table = IntegerHashTable(table_size)
        unique_nums = set(numbers)
        
        for num in unique_nums:
            hash_table.insert(num)
        
        stats = hash_table.get_statistics()
        
        # Пошук та підрахунок порівнянь
        search_numbers = random.sample(list(unique_nums), min(dataset_count // 10, len(unique_nums)))
        total_comparisons = 0
        found_count = 0
        search_time = 0
        
        start_time = time.perf_counter()
        for search_num in search_numbers:
            found, comparisons = hash_table.search(search_num)
            total_comparisons += comparisons
            if found:
                found_count += 1
        search_time = time.perf_counter() - start_time
        
        avg_comparisons = total_comparisons / len(search_numbers) if search_numbers else 0
        
        print(f"  Унікальних чисел: {stats['count']}")
        print(f"  Коефіцієнт наповненості: {stats['load_factor']:.2%}")
        print(f"  Макс. довжина ланцюжка: {stats['max_collision_chain']}")
        print(f"  Середня довжина ланцюжка: {stats['avg_collision_chain']:.2f}")
        print(f"  Пошуків виконано: {len(search_numbers)}")
        print(f"  Знайдено: {found_count}")
        print(f"  Середнє порівнянь за пошук: {avg_comparisons:.2f}")
        print(f"  Всього порівнянь: {total_comparisons}")
        print(f"  Час пошуку: {search_time*1000:.3f} мс")
        
        results.append({
            'dataset': dataset_name,
            'unique_count': stats['count'],
            'load_factor': stats['load_factor'],
            'max_chain': stats['max_collision_chain'],
            'avg_chain': stats['avg_collision_chain'],
            'avg_comparisons': avg_comparisons,
            'total_comparisons': total_comparisons,
            'search_time': search_time
        })
        
        # Видалення тестового файлу
        try:
            os.remove(filename)
        except:
            pass
    
    # Висновки
    print("\n" + "="*70)
    print("ВИСНОВКИ:")
    print("="*70)
    print(f"\n{'Набір даних':<35} {'Середній пошук':<15} {'Макс. ланцюжок':<15}")
    print("-" * 70)
    
    for result in results:
        print(f"{result['dataset']:<35} {result['avg_comparisons']:<15.2f} {result['max_chain']:<15}")
    
    print("\n" + "="*70)
    print("""
Спостереження:
  • Випадкові числа: найбільш рівномірний розподіл, мінімальні колізій
  • Відсортовані/зворотні: гірший розподіл, більше колізій через послідовні хеші
  • З дублікатами: менше унікальних чисел, але довші ланцюжки колізій
  • Скупчені: змішаний результат, залежить від положення скупчень
    """)
    print("="*70 + "\n")


if __name__ == "__main__":
    while True:
        print("\nВИБІР РЕЖИМУ РОБОТИ:")
        print("1. Побудувати таблицю та пошукати числа")
        print("2. Порівняти різні набори даних")
        print("3. Вихід")
        
        choice = input("\nВиберіть режим (1-3): ").strip()
        
        if choice == '1':
            main()
        elif choice == '2':
            compare_datasets()
        elif choice == '3':
            print("\nДо побачення!\n")
            break
        else:
            print("❌ Невірний вибір!")
