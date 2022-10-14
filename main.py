import random
from select import select
from threading import Thread
from multiprocessing import Pipe

def main():
    c1_read, c1_write = Pipe(duplex=False)
    c2_read, c2_write = Pipe(duplex=False)
    quit_read, quit_write = Pipe(duplex=False)

    def func1():        
        for i in range(10):
            c1_write.send(i)
        quit_write.send(0)

    Thread(target=func1).start()

    def func2():        
        for i in range(2):
            c2_write.send(i)
    
    Thread(target=func2).start()

    while True:
        ready, _, _ = select([c1_read, c2_read, quit_read], [], [])
        which = random.choice(ready)
            
        if which == c1_read:
            c1_read.recv()
            print('Received value from c1')
        elif which == c2_read:
            c2_read.recv()
            print('Received value from c2')
        elif which == quit_read and len(ready) == 1:
            quit_read.recv()
            print('Received value from quit')
            return

if __name__ == "__main__":
    main()