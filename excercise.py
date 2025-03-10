import threading
import time

semaphore = threading.Semaphore(0)

def process_1():
    print("P1: Starting execution")
    time.sleep(1)
    print("P1: Finished execution")
    semaphore.release()  

def process_2():
    semaphore.acquire()  
    print("P2: Starting execution")
    time.sleep(1)
    print("P2: Finished execution")

if __name__ == "__main__":
    p1 = threading.Thread(target=process_1)
    p2 = threading.Thread(target=process_2)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

