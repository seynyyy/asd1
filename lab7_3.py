import time
from typing import Tuple, Dict, List


class KeywordHashTable:
    """
    Реалізація хеш-таблиці для зарезервованих слів мови програмування
    з допомогою (HELP текстом)
    """
    
    def __init__(self, size=31):
        """
        Ініціалізація хеш-таблиці
        :param size: початкова розмірність таблиці
        """
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0
        self.restructurizations = 0
        self.insertions = 0
        self.load_factor = 0.0
    
    def hash_function(self, key):
        """
        Хеш-функція: Horner's method
        """
        h = 0
        for char in key:
            h = (h * 31 + ord(char)) % self.size
        return h
    
    def get_load_factor(self):
        """Отримати коефіцієнт наповненості таблиці"""
        self.load_factor = self.count / self.size
        return self.load_factor
    
    def insert(self, keyword, help_text, auto_restructure=True):
        """
        Вставлення ключового слова з його помічником
        :param keyword: ключове слово
        :param help_text: текст допомоги
        :param auto_restructure: автоматична реструктуризація при перевищенні порогу
        :return: кількість операцій (для порівняння)
        """
        operations = 0
        
        # Перевірка на можливість реструктуризації
        if auto_restructure and self.get_load_factor() > 0.75:
            self.restructure()
            operations = self.size // 2  # Приблизна вартість реструктуризації
        
        index = self.hash_function(keyword)
        bucket = self.table[index]
        
        # Перевірка, чи слово вже існує
        for i, (k, h) in enumerate(bucket):
            if k == keyword:
                bucket[i] = (keyword, help_text)
                operations += 1
                return operations
        
        bucket.append((keyword, help_text))
        self.count += 1
        self.insertions += 1
        operations += 1
        
        return operations
    
    def restructure(self):
        """
        Реструктуризація таблиці з збільшенням розмірності
        """
        old_table = self.table
        old_size = self.size
        
        # Новий розмір - наступне просте число
        self.size = self.find_next_prime(self.size * 2)
        self.table = [[] for _ in range(self.size)]
        self.restructurizations += 1
        
        # Переміщення всіх елементів
        for bucket in old_table:
            for keyword, help_text in bucket:
                index = self.hash_function(keyword)
                self.table[index].append((keyword, help_text))
        
        print(f"\n🔄 РЕСТРУКТУРИЗАЦІЯ ТАБЛИЦІ")
        print(f"   Стара розмірність: {old_size}")
        print(f"   Нова розмірність: {self.size}")
        print(f"   Коефіцієнт наповненості: {self.get_load_factor():.2%}\n")
    
    @staticmethod
    def find_next_prime(n):
        """Знайти наступне просте число >= n"""
        def is_prime(num):
            if num < 2:
                return False
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0:
                    return False
            return True
        
        while not is_prime(n):
            n += 1
        return n
    
    def search(self, keyword) -> Tuple[bool, str]:
        """
        Пошук ключового слова
        :return: (знайдено, текст допомоги)
        """
        index = self.hash_function(keyword)
        bucket = self.table[index]
        
        for k, h in bucket:
            if k == keyword:
                return True, h
        
        return False, ""
    
    def delete(self, keyword) -> bool:
        """
        Видалення ключового слова
        """
        index = self.hash_function(keyword)
        bucket = self.table[index]
        
        for i, (k, h) in enumerate(bucket):
            if k == keyword:
                bucket.pop(i)
                self.count -= 1
                return True
        
        return False
    
    def display(self):
        """
        Вивід таблиці на екран
        """
        print("\n" + "="*80)
        print(f"ХЕШ-ТАБЛИЦЯ ЗАРЕЗЕРВОВАНИХ СЛІВ (Розмір: {self.size})")
        print("="*80)
        
        for i, bucket in enumerate(self.table):
            if bucket:
                print(f"\n[Індекс {i:3}]")
                for keyword, help_text in bucket:
                    help_preview = help_text[:60] + "..." if len(help_text) > 60 else help_text
                    print(f"  ► {keyword:20} : {help_preview}")
        
        print(f"\n{'='*80}")
        print(f"Всього слів: {self.count} | Розмір: {self.size} | Коефіцієнт наповненості: {self.get_load_factor():.2%}")
        print(f"Реструктуризацій: {self.restructurizations} | Вставок: {self.insertions}")
        print(f"{'='*80}\n")
    
    def get_statistics(self):
        """
        Отримати детальну статистику таблиці
        """
        bucket_sizes = [len(bucket) for bucket in self.table]
        non_empty = sum(1 for b in bucket_sizes if b > 0)
        max_collision = max(bucket_sizes) if bucket_sizes else 0
        
        return {
            'size': self.size,
            'count': self.count,
            'load_factor': self.get_load_factor(),
            'non_empty_buckets': non_empty,
            'max_collision': max_collision,
            'restructurizations': self.restructurizations,
            'insertions': self.insertions
        }


def initialize_python_keywords():
    """
    Ініціалізація таблиці з зарезервованих слів Python
    """
    keywords = {
        'if': 'Оператор умовного розгалуження для перевірки умов',
        'else': 'Частина умовного оператора, виконується якщо умова хибна',
        'elif': 'Додаткова умова в ланцюжку умовних операторів',
        'for': 'Цикл для проходження по послідовності або діапазону',
        'while': 'Цикл з умовою, повторяється поки умова істинна',
        'break': 'Оператор для переривання циклу',
        'continue': 'Оператор для пропуску поточної ітерації циклу',
        'def': 'Оператор для визначення функції',
        'return': 'Повертає значення з функції',
        'class': 'Визначає новий клас',
        'import': 'Імпортує модуль або об\'єкт з модуля',
        'from': 'Імпортує конкретні об\'єкти з модуля',
        'as': 'Дає альтернативну назву імпортованому модулю чи об\'єкту',
        'try': 'Позначає блок для обробки винятків',
        'except': 'Перехоплює виняток із вказаного типу',
        'finally': 'Виконується завжди, незалежно від результату try/except',
        'raise': 'Генерує виняток',
        'with': 'Контекстний менеджер для автоматичного управління ресурсами',
        'lambda': 'Створює анонімну функцію',
        'pass': 'Оператор, який нічого не робить',
        'assert': 'Перевіряє умову, підіймає AssertionError якщо вона хибна',
        'global': 'Оголошує змінну як глобальну',
        'nonlocal': 'Оголошує змінну як нелокальну (з зовнішної області видимості)',
        'yield': 'Перетворює функцію на генератор',
        'is': 'Перевіряє, чи два об\'єкти мають однакову ідентичність',
        'in': 'Перевіряє наявність елемента в послідовності',
        'not': 'Логічне заперечення',
        'and': 'Логічне "І"',
        'or': 'Логічне "АБО"'
    }
    
    return keywords


def show_help(hash_table, keyword):
    """
    Показати помічник для ключового слова
    """
    found, help_text = hash_table.search(keyword.lower())
    
    if found:
        print(f"\n{'='*80}")
        print(f"ДОПОМОГА: {keyword.upper()}")
        print(f"{'='*80}")
        print(f"{help_text}")
        print(f"{'='*80}\n")
    else:
        print(f"\n❌ Слово '{keyword}' не знайдено в таблиці!\n")


def add_new_keyword(hash_table):
    """
    Додати нове ключове слово
    """
    print("\n" + "-"*80)
    print("ДОДАВАННЯ НОВОГО КЛЮЧОВОГО СЛОВА")
    print("-"*80)
    
    keyword = input("Введіть ключове слово: ").strip().lower()
    
    if not keyword:
        print("❌ Ключове слово не може бути пустим!\n")
        return
    
    found, _ = hash_table.search(keyword)
    if found:
        print(f"❌ Слово '{keyword}' вже існує в таблиці!\n")
        return
    
    help_text = input("Введіть текст допомоги: ").strip()
    
    if not help_text:
        print("❌ Текст допомоги не може бути пустим!\n")
        return
    
    # Вставлення з реструктуризацією якщо потрібно
    old_size = hash_table.size
    hash_table.insert(keyword, help_text, auto_restructure=True)
    
    if hash_table.size > old_size:
        print(f"✓ Слово '{keyword}' додане! (проведена реструктуризація)")
    else:
        print(f"✓ Слово '{keyword}' додане без реструктуризації!")
    
    print(f"Поточний коефіцієнт наповненості: {hash_table.get_load_factor():.2%}\n")


def compare_efficiency():
    """
    Порівняння ефективності додавання та реструктуризації
    """
    print("\n" + "="*80)
    print("ПОРІВНЯННЯ ЕФЕКТИВНОСТІ ДОДАВАННЯ ТА РЕСТРУКТУРИЗАЦІЇ")
    print("="*80 + "\n")
    
    fill_factors = [0.25, 0.50, 0.75, 0.90]
    results = []
    
    for fill_factor in fill_factors:
        print(f"Тестування для коефіцієнта наповненості: {fill_factor:.0%}")
        print("-" * 80)
        
        # Таблиця БЕЗ автоматичної реструктуризації
        table_no_restr = KeywordHashTable(31)
        keywords = initialize_python_keywords()
        
        target_count = int(31 * fill_factor)
        keywords_list = list(keywords.items())[:target_count]
        
        for keyword, help_text in keywords_list:
            table_no_restr.insert(keyword, help_text, auto_restructure=False)
        
        # Вимірювання часу додавання БЕЗ реструктуризації
        start_time = time.perf_counter()
        for i in range(10):
            table_no_restr.insert(f"test_{i}", f"Test keyword {i}", auto_restructure=False)
        time_no_restr = time.perf_counter() - start_time
        
        # Таблиця З автоматичною реструктуризацією
        table_with_restr = KeywordHashTable(31)
        
        for keyword, help_text in keywords_list:
            table_with_restr.insert(keyword, help_text, auto_restructure=True)
        
        # Вимірювання часу додавання З реструктуризацією
        start_time = time.perf_counter()
        for i in range(10):
            table_with_restr.insert(f"test_{i}", f"Test keyword {i}", auto_restructure=True)
        time_with_restr = time.perf_counter() - start_time
        
        stats_no_restr = table_no_restr.get_statistics()
        stats_with_restr = table_with_restr.get_statistics()
        
        print(f"\nБЕЗ реструктуризації:")
        print(f"  Розмір таблиці: {stats_no_restr['size']}")
        print(f"  Слів в таблиці: {stats_no_restr['count']}")
        print(f"  Коефіцієнт наповненості: {stats_no_restr['load_factor']:.2%}")
        print(f"  Час додавання 10 слів: {time_no_restr*1000:.3f} мс")
        print(f"  Макс. довжина ланцюжка: {stats_no_restr['max_collision']}")
        
        print(f"\nЗ автоматичною реструктуризацією:")
        print(f"  Розмір таблиці: {stats_with_restr['size']}")
        print(f"  Слів в таблиці: {stats_with_restr['count']}")
        print(f"  Коефіцієнт наповненості: {stats_with_restr['load_factor']:.2%}")
        print(f"  Час додавання 10 слів: {time_with_restr*1000:.3f} мс")
        print(f"  Реструктуризацій: {stats_with_restr['restructurizations']}")
        print(f"  Макс. довжина ланцюжка: {stats_with_restr['max_collision']}")
        
        difference = ((time_no_restr - time_with_restr) / time_no_restr * 100) if time_no_restr > 0 else 0
        print(f"\nРізниця у часі: {abs(difference):.1f}% {'швидше' if difference > 0 else 'повільніше'} з реструктуризацією")
        
        results.append({
            'fill_factor': fill_factor,
            'time_no_restr': time_no_restr,
            'time_with_restr': time_with_restr,
            'size_no_restr': stats_no_restr['size'],
            'size_with_restr': stats_with_restr['size'],
            'collisions_no_restr': stats_no_restr['max_collision'],
            'collisions_with_restr': stats_with_restr['max_collision']
        })
        
        print("\n")
    
    # Загальний висновок
    print("="*80)
    print("ВИСНОВКИ:")
    print("="*80)
    print("""
Реструктуризація таблиці:
  ✓ Зменшує максимальну довжину ланцюжків (зменшує коліцій)
  ✓ Покращує середній час пошуку
  ✓ На малих коефіцієнтах наповненості коліцій мало, тому реструктуризація 
    не дає великого виграшу
  ✓ На великих коефіцієнтах (>75%) реструктуризація істотно покращує 
    продуктивність

Рекомендація:
  - Оптимальний коефіцієнт наповненості: 0.5 - 0.75
  - Запускати реструктуризацію, коли коефіцієнт перевищує 0.75
  - Збільшувати розмір до наступного простого числа
    """)
    print("="*80 + "\n")


def main():
    """
    Основна функція програми
    """
    print("\n" + "="*80)
    print("ПРОГРАМА: ХЕШ-ТАБЛИЦЯ ЗАРЕЗЕРВОВАНИХ СЛІВ МОВИ ПРОГРАМУВАННЯ")
    print("="*80 + "\n")
    
    # Ініціалізація таблиці
    hash_table = KeywordHashTable(31)
    keywords = initialize_python_keywords()
    
    print(f"Ініціалізація таблиці з {len(keywords)} ключовими словами Python...\n")
    
    for keyword, help_text in keywords.items():
        hash_table.insert(keyword, help_text, auto_restructure=True)
    
    # Основний цикл програми
    while True:
        print("\nВИБІР ОПЕРАЦІЇ:")
        print("1. Показати допомогу для слова")
        print("2. Додати нове ключове слово")
        print("3. Показати всю таблицю")
        print("4. Показати статистику таблиці")
        print("5. Видалити ключове слово")
        print("6. Порівняти ефективність")
        print("7. Вихід")
        
        choice = input("\nВиберіть операцію (1-7): ").strip()
        
        if choice == '1':
            keyword = input("\nВведіть ключове слово для пошуку: ").strip()
            if keyword:
                show_help(hash_table, keyword)
        
        elif choice == '2':
            add_new_keyword(hash_table)
        
        elif choice == '3':
            hash_table.display()
        
        elif choice == '4':
            stats = hash_table.get_statistics()
            print(f"\n{'СТАТИСТИКА ТАБЛИЦІ':^80}")
            print("="*80)
            print(f"Розмірність таблиці: {stats['size']}")
            print(f"Всього ключових слів: {stats['count']}")
            print(f"Коефіцієнт наповненості: {stats['load_factor']:.2%}")
            print(f"Занятих клітинок: {stats['non_empty_buckets']}")
            print(f"Максимальна довжина ланцюжка: {stats['max_collision']}")
            print(f"Всього реструктуризацій: {stats['restructurizations']}")
            print(f"Всього вставок: {stats['insertions']}")
            print("="*80 + "\n")
        
        elif choice == '5':
            keyword = input("\nВведіть ключове слово для видалення: ").strip().lower()
            if hash_table.delete(keyword):
                print(f"✓ Слово '{keyword}' видалено!\n")
            else:
                print(f"❌ Слово '{keyword}' не знайдено!\n")
        
        elif choice == '6':
            compare_efficiency()
        
        elif choice == '7':
            print("\nДо побачення!\n")
            break
        
        else:
            print("❌ Невірний вибір!")


if __name__ == "__main__":
    main()
