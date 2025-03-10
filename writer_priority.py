import time
import random
import multiprocessing

def reader(reader_id, active_readers, waiting_writers, active_writers, mutex, ok_to_read, ok_to_write):
    while True:
        time.sleep(random.uniform(0.5, 2))
        print(f"Reader {reader_id} wants to access the critical section.")

        with mutex:
            while active_writers.value > 0 or waiting_writers.value > 0:
                print(f"Reader {reader_id} is waiting due to writer priority.")
                ok_to_read.wait()
            active_readers.value += 1

        print(f"Reader {reader_id} is reading data...")
        time.sleep(random.uniform(1, 3))

        with mutex:
            active_readers.value -= 1
            if active_readers.value == 0 and waiting_writers.value > 0:
                ok_to_write.notify()
        print(f"Reader {reader_id} has finished reading.")


def writer(writer_id, active_readers, waiting_writers, active_writers, mutex, ok_to_read, ok_to_write):
    while True:
        time.sleep(random.uniform(1, 3))
        print(f"Writer {writer_id} wants to access the critical section.")

        with mutex:
            waiting_writers.value += 1
            while active_writers.value > 0 or active_readers.value > 0:
                print(f"Writer {writer_id} is waiting for readers/writers to finish.")
                ok_to_write.wait()
            waiting_writers.value -= 1
            active_writers.value += 1

        print(f"Writer {writer_id} is writing data...")
        time.sleep(random.uniform(2, 4))

        with mutex:
            active_writers.value -= 1
            if waiting_writers.value > 0:
                ok_to_write.notify()
            else:
                ok_to_read.notify_all()
        print(f"Writer {writer_id} has finished writing.")


if __name__ == "__main__":
    active_readers = multiprocessing.Value('i', 0)
    active_writers = multiprocessing.Value('i', 0)
    waiting_writers = multiprocessing.Value('i', 0)

    mutex = multiprocessing.Lock()
    ok_to_read = multiprocessing.Condition(mutex)
    ok_to_write = multiprocessing.Condition(mutex)

    reader_processes = [multiprocessing.Process(target=reader, args=(i, active_readers, waiting_writers, active_writers, mutex, ok_to_read, ok_to_write)) for i in range(3)]
    writer_processes = [multiprocessing.Process(target=writer, args=(i, active_readers, waiting_writers, active_writers, mutex, ok_to_read, ok_to_write)) for i in range(2)]

    for r in reader_processes:
        r.start()
    for w in writer_processes:
        w.start()

    for r in reader_processes:
        r.join()
    for w in writer_processes:
        w.join()
