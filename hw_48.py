import os
import random
import string
from threading import Thread
import numpy as np
import time


def file_generator(directory, number_of_files, size):
    if not os.path.exists(directory):
        os.mkdir(directory)

    for number in range(number_of_files):
        with open(f'{directory}/file_{number}.txt', 'w') as file:
            file.write(generate_random_string_for_file(size))


def generate_random_string_for_file(size):
    random_content_size = random.randint(int(size / 2), size)
    return ''.join(random.choices(string.printable, k=random_content_size))


def letter_counter_in_one_thread(directory, letter_to_find):
    filelist = os.listdir(directory)
    result = 0
    for current_file in filelist:
        with open(f'{directory}/{current_file}', 'r') as file:
            result += file.read().count(letter_to_find)

    return result


def letter_counter_in_n_threads(directory, letter_to_find, number_of_threads):
    def letter_counter_in_thread(directory, letter_to_find, letters_in_file, filelist):
        result = 0
        for current_file in filelist:
            with open(f'{directory}/{current_file}', 'r') as file:
                result = file.read().count(letter_to_find)
        letters_in_file.append(result)

    threads = []
    filelist = os.listdir(directory)
    splitted_files_list = np.array_split(filelist, number_of_threads)

    for i in range(number_of_threads):
        new_thread = Thread(target=letter_counter_in_thread,
                            args=(directory, letter_to_find, letters_in_file, splitted_files_list[i].tolist()))
        threads.append(new_thread)
        new_thread.start()

    for i in threads:
        i.join()

    return sum(letters_in_file)


def count_function_time(function, *args, **kwargs):
    start_time = time.time()
    function(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"{function.__name__} working time = " + str(execution_time))


directory_name = 'data'
directory_path = f'./{directory_name}'
file_numbers = 3
file_size = 199
symbol_to_find = '1'
thread_numbers = 5

letters_in_file = []

file_generator(directory_path, file_numbers, file_size)
print("found symbols = " + str(letter_counter_in_one_thread(directory_path, symbol_to_find)))
print("found symbols = " + str(letter_counter_in_n_threads(directory_path, symbol_to_find, thread_numbers)))
count_function_time(letter_counter_in_one_thread, directory_path, symbol_to_find)
count_function_time(letter_counter_in_n_threads, directory_path, symbol_to_find, thread_numbers)

