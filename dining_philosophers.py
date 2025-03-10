import threading
import time

N = 5  
THINKING = 2
HUNGRY = 1
EATING = 0
LEFT = lambda phnum: (phnum + N - 1) % N
RIGHT = lambda phnum: (phnum + 1) % N

state = [THINKING] * N
mutex = threading.Lock()
S = [threading.Condition(mutex) for _ in range(N)]

def test(phnum):
    if state[phnum] == HUNGRY and state[LEFT(phnum)] != EATING and state[RIGHT(phnum)] != EATING:
        state[phnum] = EATING
        print(f"Philosopher {phnum + 1} takes fork {LEFT(phnum) + 1} and {phnum + 1}")
        print(f"Philosopher {phnum + 1} is Eating")
        S[phnum].notify()

def take_fork(phnum):
    with mutex:
        state[phnum] = HUNGRY
        print(f"Philosopher {phnum + 1} is Hungry")
        test(phnum)
        while state[phnum] != EATING:
            S[phnum].wait()

def put_fork(phnum):
    with mutex:
        state[phnum] = THINKING
        print(f"Philosopher {phnum + 1} putting fork {LEFT(phnum) + 1} and {phnum + 1} down")
        print(f"Philosopher {phnum + 1} is thinking")
        test(LEFT(phnum))
        test(RIGHT(phnum))

def philosopher(phnum):
    while True:
        time.sleep(1) 
        take_fork(phnum)
        time.sleep(2)  
        put_fork(phnum)

if __name__ == "__main__":
    threads = []
    for i in range(N):
        print(f"Philosopher {i + 1} is thinking")
        t = threading.Thread(target=philosopher, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
