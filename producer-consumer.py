import threading
import time
import random

buffer = []
buffer_size = 30
buffer_lock = threading.Lock()
empty_slots = threading.Semaphore(buffer_size)
filled_slots = threading.Semaphore(0)

def producer(producer_id):
    while True:
        time.sleep(random.uniform(0.1, 1))
        item = random.randint(0, 100)
        empty_slots.acquire()
        with buffer_lock:
            buffer.append(item)
            print(f"Producer-{producer_id} produced item: {item}. Buffer size: {len(buffer)}")
        filled_slots.release()

def consumer(consumer_id):
    while True:
        time.sleep(random.uniform(0.2, 2))
        filled_slots.acquire()
        with buffer_lock:
            item = buffer.pop(0)
            print(f"Consumer-{consumer_id} consumed item: {item}. Buffer size: {len(buffer)}")
        empty_slots.release()

def main():
    for i in range(3):
        threading.Thread(target=producer, args=(i+1,), name=f"Producer-{i+1}").start()

    for i in range(5):
        threading.Thread(target=consumer, args=(i+1,), name=f"Consumer-{i+1}").start()

if __name__ == "__main__":
    main()
