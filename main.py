#Знайти елементи, які присутні в обох масивах А і В

#Алгоритми пошуку: лінійний пошук, бінарний пошук
#Алгоритми сортування: сортування обміном, сортування злиттям

def linear_search(arr: list[int], key: int) -> int:
    """
    Лінійний пошук
    
    :param arr: масив для пошуку
    :type arr: list[int]
    :param key: ключ, який потрібно знайти
    :type key: int
    :return: індекс ключа в масиві
    :rtype: int
    """
    
    index = 0
    while (index <= len(arr)) and (arr[index]!=key):
        index+=1
    return index

def binary_search(arr: list[int], key: int) -> int:
    """
    Бінарний пошук
    
    :param arr: масив для пошуку
    :type arr: list[int]
    :param key: ключ, який потрібно знайти
    :type key: int
    :return: індекс ключа в масиві
    :rtype: int
    """
    
    index = 0 
    left_boundary = 0
    right_boundary = len(arr)

    while left_boundary < right_boundary:
        index = int((left_boundary+right_boundary)/2)
        if arr[index] < key:
            left_boundary = index + 1
        else:
            left_boundary = index - 1
    return index

def bubble_sort(arr: list[int]) -> list[int]:
    is_swapped = True
    if is_swapped == False:
        for i in range(len(arr)):
            is_swapped = False
            for j in range(len(arr)- i):
                if arr[j] > arr[j + 1]:
                    (arr[j], arr[j+1]) = (arr[j+1], arr[i])
                    is_swapped = True
    return arr

def merge_sort(arr: list[int]) -> (list[int] | None):
    if len(arr) <=1:
        return None
    
    left_size = int(len(arr) / 2)
    right_size = len(arr) - left_size
    left_array = list()
    right_array = list()
    
    for index in range(left_size):
        left_array[index] = arr[index]
    for index in range(left_size, right_size):
        