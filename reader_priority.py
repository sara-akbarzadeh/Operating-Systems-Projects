import multiprocessing
import time
import random

def read(reader_id, resource_mutex, reader_count_mutex, current_readers):
    with reader_count_mutex:
        current_readers.value += 1
        if current_readers.value == 1:
            resource_mutex.acquire()

    print(f"Reader {reader_id} is reading...")
    time.sleep(1)
    print(f"Reader {reader_id} has finished reading.")

    with reader_count_mutex:
        current_readers.value -= 1
        if current_readers.value == 0:
            resource_mutex.release()

def write(writer_id, resource_mutex, waiting_writers):
    with waiting_writers.get_lock():
        waiting_writers.value += 1

    resource_mutex.acquire()
    with waiting_writers.get_lock():
        waiting_writers.value -= 1

    print(f"Writer {writer_id} is writing...")
    time.sleep(2)
    print(f"Writer {writer_id} has finished writing.")

    resource_mutex.release()

def reader_task(reader_id, resource_mutex, reader_count_mutex, current_readers):
    while True:
        time.sleep(random.randint(1, 3))
        read(reader_id, resource_mutex, reader_count_mutex, current_readers)

def writer_task(writer_id, resource_mutex, waiting_writers):
    while True:
        time.sleep(random.randint(2, 5))
        write(writer_id, resource_mutex, waiting_writers)

if __name__ == "__main__":
    resource_mutex = multiprocessing.Lock()
    reader_count_mutex = multiprocessing.Lock()
    current_readers = multiprocessing.Value('i', 0)
    waiting_writers = multiprocessing.Value('i', 0)

    readers = [multiprocessing.Process(target=reader_task, args=(i, resource_mutex, reader_count_mutex, current_readers)) for i in range(5)]
    writers = [multiprocessing.Process(target=writer_task, args=(i, resource_mutex, waiting_writers)) for i in range(3)]

    all_processes = readers + writers
    random.shuffle(all_processes)

    for p in all_processes:
        p.start()

    for p in all_processes:
        p.join()
