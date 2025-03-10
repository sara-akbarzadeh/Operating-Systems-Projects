import threading
import time

semaphore_a = threading.Semaphore(1)
semaphore_b = threading.Semaphore(1)

def thread_1():
    print("Thread 1: Waiting for semaphore A")
    semaphore_a.acquire()
    print("Thread 1: Acquired semaphore A")
    time.sleep(1)
    print("Thread 1: Waiting for semaphore B")
    semaphore_b.acquire()
    print("Thread 1: Acquired semaphore B")
    semaphore_b.release()
    semaphore_a.release()
    print("Thread 1: Released both semaphores")

def thread_2():
    print("Thread 2: Waiting for semaphore B")
    semaphore_b.acquire()
    print("Thread 2: Acquired semaphore B")
    time.sleep(1)
    print("Thread 2: Waiting for semaphore A")
    semaphore_a.acquire()
    print("Thread 2: Acquired semaphore A")
    semaphore_a.release()
    semaphore_b.release()
    print("Thread 2: Released both semaphores")

def main():
    t1 = threading.Thread(target=thread_1, name="Thread-1")
    t2 = threading.Thread(target=thread_2, name="Thread-2")
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == "__main__":
    main()
