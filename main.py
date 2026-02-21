import random
import timeit
from tabulate import tabulate

#Знайти елементи, які присутні в обох масивах А і В

#Алгоритми пошуку: лінійний пошук, бінарний пошук
#Алгоритми сортування: сортування обміном, сортування злиттям

def measure_time(sort_func, data):
    start_time = timeit.default_timer()
    sorted_data = sort_func(data[:])
    execution_time = timeit.default_timer() - start_time
    return sorted_data, execution_time

def measure_search_time(search_func, arr, key):
    """Вимірювання часу виконання пошуку"""
    start_time = timeit.default_timer()
    result = search_func(arr, key)
    execution_time = timeit.default_timer() - start_time
    return result, execution_time

def find_common_elements_linear(arr_a: list[int], arr_b: list[int]) -> list[int]:
    """
    Знаходить елементи, присутні в обох масивах, використовуючи лінійний пошук
    
    :param arr_a: перший масив
    :param arr_b: другий масив
    :return: список спільних елементів
    """
    common = []
    for elem in arr_a:
        if linear_search(arr_b, elem) != -1 and elem not in common:
            common.append(elem)
    return common

def find_common_elements_binary(arr_a: list[int], arr_b_sorted: list[int]) -> list[int]:
    """
    Знаходить елементи, присутні в обох масивах, використовуючи бінарний пошук
    (arr_b має бути відсортованим)
    
    :param arr_a: перший масив
    :param arr_b_sorted: другий масив (відсортований)
    :return: список спільних елементів
    """
    common = []
    for elem in arr_a:
        if binary_search(arr_b_sorted, elem) != -1 and elem not in common:
            common.append(elem)
    return common

def linear_search(arr: list[int], key: int) -> int:
    """
    Лінійний пошук
    
    :param arr: масив для пошуку
    :type arr: list[int]
    :param key: ключ, який потрібно знайти
    :type key: int
    :return: індекс ключа в масиві або -1 якщо не знайдено
    :rtype: int
    """
    
    for index in range(len(arr)):
        if arr[index] == key:
            return index
    return -1

def binary_search(arr: list[int], key: int) -> int:
    """
    Бінарний пошук
    
    :param arr: масив для пошуку
    :type arr: list[int]
    :param key: ключ, який потрібно знайти
    :type key: int
    :return: індекс ключа в масиві або -1 якщо не знайдено
    :rtype: int
    """
    
    left_boundary = 0
    right_boundary = len(arr) - 1

    while left_boundary <= right_boundary:
        index = (left_boundary + right_boundary) // 2
        if arr[index] == key:
            return index
        elif arr[index] < key:
            left_boundary = index + 1
        else:
            right_boundary = index - 1
    return -1

def bubble_sort(arr: list[int]) -> list[int]:
    arr = arr[:]
    n = len(arr)
    for i in range(n):
        is_swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                is_swapped = True
        if not is_swapped:
            break
    return arr

def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr[:]
    
    arr = arr[:]
    mid = len(arr) // 2
    left_array = merge_sort(arr[:mid])
    right_array = merge_sort(arr[mid:])
    
    return merge(left_array, right_array)

def merge(left_array: list[int], right_array: list[int]) -> list[int]:
    merge_array = []
    left_index = 0
    right_index = 0

    while left_index < len(left_array) and right_index < len(right_array):
        if left_array[left_index] <= right_array[right_index]:
            merge_array.append(left_array[left_index])
            left_index += 1
        else:
            merge_array.append(right_array[right_index])
            right_index += 1
    
    merge_array.extend(left_array[left_index:])
    merge_array.extend(right_array[right_index:])
    return merge_array

# def generate_array(count: int) -> list[int]:
#     array = list()
#     for i in range(0, count-1):
#         array.append(randint(0, count*10))
#     return array

# def generate_big_arrays() -> tuple[list[int], list[int], list[int]]:
#     """
#     Створює 3 масиви на 10000 елементів
    
#     :return: 
#         Невідсортований масив, 
#         Відсортований в протилежому порядку, 
#         Майже відсортований
#     :rtype: (list[int], list[int], list[int])
#     """
#     array_reversed = list()
#     array_reversed.append(100000)
#     for i in range(1, 10000):
#         array_reversed.append(randint(array_reversed[i-1]-1000, array_reversed[i-1]))
        
#     array_almost_sorted = array_reversed.copy()
#     array_almost_sorted.reverse()
#     for i in range(1000):
#         index_1 = randint(0, 9999)
#         index_2 = randint(0, 9999)
#         (array_almost_sorted[index_1], array_almost_sorted[index_2]) = (array_almost_sorted[index_2], array_almost_sorted[index_1])
            
#     array_unsorted = array_reversed.copy()
#     last_index = 0
#     for i in range(5000):
#         next_index = randint(0, 9999)
#         (array_unsorted[last_index], array_unsorted[next_index]) = (array_unsorted[next_index], array_unsorted[last_index])
#         last_index = next_index
#     return (array_unsorted, array_reversed, array_almost_sorted)

if __name__ == "__main__":
    print("\n" + "="*80)
    print("ЛАБОРАТОРНА РОБОТА: АЛГОРИТМИ СОРТУВАННЯ ТА ПОШУКУ")
    print("Індивідуальне завдання: Знайти елементи, які присутні в обох масивах А і В")
    print("="*80 + "\n")
    
    # Генерація масивів
    print("Етап 1: Генерація масивів...")
    data_smallest = [random.randint(0, 100) for _ in range(10)]
    data_small = [random.randint(0, 100) for _ in range(100)]
    data_big = [random.randint(0, 500) for _ in range(1_000)]
    data_largest = [random.randint(0, 10_000) for _ in range(10_000)]
    
    # Варіації найбільшого масиву
    data_almost_sorted = sorted(data_largest.copy())
    swap_count = len(data_almost_sorted) // 10  # 10% елементів
    for _ in range(swap_count):
        i, j = random.randint(0, len(data_almost_sorted)-1), random.randint(0, len(data_almost_sorted)-1)
        data_almost_sorted[i], data_almost_sorted[j] = data_almost_sorted[j], data_almost_sorted[i]

    data_reversed = sorted(data_largest.copy(), reverse=True)
    
    # Вивід невідсортованих масивів
    print("\nНЕВІДСОРТОВАНІ МАСИВИ:")
    print("-" * 80)
    print(f"Масив 10 елементів: {data_smallest}")
    print(f"Масив 100 елементів (перші 20): {data_small[:20]}...")
    print(f"Масив 1000 елементів (перші 20): {data_big[:20]}...")
    print(f"Масив 10000 елементів (перші 20): {data_largest[:20]}...")
    print(f"Майже відсортований (перші 20): {data_almost_sorted[:20]}...")
    print(f"Зворотній порядок (перші 20): {data_reversed[:20]}...")
    print("-" * 80 + "\n")
    
    test_data = [
        ("10 елементів", data_smallest),
        ("100 елементів", data_small),
        ("1000 елементів", data_big),
        ("10000 елементів", data_largest),
        ("Майже відсорт.", data_almost_sorted),
        ("Зворотній", data_reversed)
    ]

    # Порівняння алгоритмів сортування
    print("\nЕтап 2: Порівняння алгоритмів сортування...\n")
    sorting_functions = [
        ("Bubble Sort", bubble_sort),
        ("Merge Sort", merge_sort),
        ("Timsort (sorted)", sorted)
    ]
    
    sort_table = []
    sort_headers = ["Алгоритм"] + [name for name, _ in test_data]

    for sort_name, sort_func in sorting_functions:
        row = [sort_name]
        for _, data in test_data:
            _, exec_time = measure_time(sort_func, data)
            row.append(f"{exec_time:.6f}s")
        sort_table.append(row)

    print("ТАБЛИЦЯ РЕЗУЛЬТАТІВ СОРТУВАННЯ (час виконання):")
    print(tabulate(sort_table, headers=sort_headers, tablefmt="github"))
    
    # Етап 3: Пошук в відсортованому масиві на 10000 елементів
    print("\n" + "="*80)
    print("Етап 3: ПОШУК В ВІДСОРТОВАНОМУ МАСИВІ (10000 елементів)")
    print("="*80 + "\n")
    
    # Сортуємо масив на 10000 елементів
    sorted_large_array = sorted(data_largest)
    print(f"Відсортований масив (перші 30 елементів): {sorted_large_array[:30]}...")
    print(f"Відсортований масив (останні 30 елементів): ...{sorted_large_array[-30:]}\n")
    
    # Елементи для пошуку
    search_elements = [
        (sorted_large_array[100], "Елемент на позиції 100"),
        (sorted_large_array[5000], "Елемент в середині (поз. 5000)"),
        (sorted_large_array[9999], "Останній елемент"),
        (sorted_large_array[0], "Перший елемент"),
        (-1, "Неіснуючий елемент (мін)"),
        (99999, "Неіснуючий елемент (макс)")
    ]
    
    print("Пошук елементів у відсортованому масиві на 10000 елементів:\n")
    search_results_table = []
    search_results_headers = ["Елемент", "Знач.", "Лінійний (індекс)", "Час (лін.)", "Бінарний (індекс)", "Час (бін.)", "Прискорення"]
    
    for element, description in search_elements:
        # Лінійний пошук
        idx_linear, time_linear = measure_search_time(linear_search, sorted_large_array, element)
        
        # Бінарний пошук
        idx_binary, time_binary = measure_search_time(binary_search, sorted_large_array, element)
        
        # Визначення індексу для відображення
        linear_result = idx_linear if idx_linear != -1 and idx_linear < len(sorted_large_array) else "Не знайдено"
        binary_result = idx_binary if idx_binary != -1 else "Не знайдено"
        
        speedup = f"{time_linear / time_binary:.2f}x" if time_binary > 0 else "N/A"
        
        search_results_table.append([
            description,
            element,
            linear_result,
            f"{time_linear:.7f}s",
            binary_result,
            f"{time_binary:.7f}s",
            speedup
        ])
    
    print(tabulate(search_results_table, headers=search_results_headers, tablefmt="github"))
    
    print("-" * 80 + "\n")
    
    # Створення масивів А і В для індивідуального завдання
    print("="*80)
    print("Етап 4: ІНДИВІДУАЛЬНЕ ЗАВДАННЯ - Пошук спільних елементів")
    print("="*80 + "\n")
    
    array_a = [random.randint(0, 50) for _ in range(20)]
    array_b = [random.randint(0, 50) for _ in range(20)]
    
    print(f"Масив A: {array_a}")
    print(f"Масив B: {array_b}")
    
    # Пошук у несортованих масивах
    print("\nПошук у НЕСОРТОВАНИХ масивах (лінійний пошук):")
    common_linear, time_linear = measure_search_time(find_common_elements_linear, array_a, array_b)
    print(f"Знайдені спільні елементи: {sorted(common_linear) if common_linear else 'Відсутні'}")
    print(f"Час виконання: {time_linear:.6f}s")
    print(f"Кількість спільних елементів: {len(common_linear)}")
    
    # Пошук у відсортованих масивах
    print("\nПошук у ВІДСОРТОВАНИХ масивах (бінарний пошук):")
    array_b_sorted = sorted(array_b)
    common_binary, time_binary = measure_search_time(find_common_elements_binary, array_a, array_b_sorted)
    print(f"Відсортований масив B: {array_b_sorted}")
    print(f"Знайдені спільні елементи: {sorted(common_binary) if common_binary else 'Відсутні'}")
    print(f"Час виконання: {time_binary:.6f}s")
    print(f"Кількість спільних елементів: {len(common_binary)}")
    
    if not common_linear:
        print("\n⚠ ПОВІДОМЛЕННЯ: Спільні елементи в масивах А і В відсутні")
    
    # Порівняння пошуку на різних розмірах
    print("\n" + "="*80)
    print("Етап 5: Порівняння ефективності пошуку на різних масивах")
    print("="*80 + "\n")
    
    search_table = []
    search_headers = ["Розмір масиву", "Лінійний (несорт.)", "Бінарний (сорт.)", "Прискорення"]
    
    for name, data in test_data:
        # Створюємо два масиви для пошуку спільних елементів
        test_a = data[:len(data)//2]
        test_b = data[len(data)//2:]
        
        # Лінійний пошук на несортованих
        _, time_lin = measure_search_time(find_common_elements_linear, test_a, test_b)
        
        # Бінарний пошук на відсортованих
        test_b_sorted = sorted(test_b)
        _, time_bin = measure_search_time(find_common_elements_binary, test_a, test_b_sorted)
        
        speedup = time_lin / time_bin if time_bin > 0 else 0
        search_table.append([name, f"{time_lin:.6f}s", f"{time_bin:.6f}s", f"{speedup:.2f}x"])
    
    print("ТАБЛИЦЯ РЕЗУЛЬТАТІВ ПОШУКУ:")
    print(tabulate(search_table, headers=search_headers, tablefmt="github"))

    print("="*80 + "\n")