# Multi-processing using Golang-like channels

Let's create the channels to paste the data to be processed elsewhere in the application.
In this example, we will use Pipe to paste data between channels.

Example of this implementation in Go:

```go
package main

import "fmt"

func main() {
    c1 := make(chan int)
    c2 := make(chan int)
    quit := make(chan int)

    go func() {
        for i := 0; i < 10; i++ {
            c1 <- i
        }
        quit <- 0
    }()

    go func() {
        for i := 0; i < 2; i++ {
            c2 <- i
        }
    }()

    for {
        select {
        case <-c1:
            fmt.Println("Received value from c1")
        case <-c2:
            fmt.Println("Received value from c2")
        case <-quit:
            fmt.Println("quit")
            return
        }
    }
}

// Output:
Received value from c1
Received value from c1
Received value from c2
Received value from c1
Received value from c2
Received value from c1
Received value from c1
Received value from c1
Received value from c1
Received value from c1
Received value from c1
Received value from c1
quit
```
In python can has more then one examples, depends on the resource that you being to use:

One idea or solution is using Pipe of multiprocessor.

Example:

```python
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

# Output:
Received value from c1
Received value from c1
Received value from c2
Received value from c1
Received value from c2
Received value from c1
Received value from c1
Received value from c1
Received value from c1
Received value from c1
Received value from c1
Received value from c1
Received value from quit
```

Other way to create the same example is using `goless`

Example:

```python
import time
import goless

def main():
    c1 = goless.chan()
    c2 = goless.chan()

    def func1():        
        for i in range(10):            
            c1.send(i)
            time.sleep(1)

    goless.go(func1)        

    def func2():
        for i in range(5):
            c2.send(i)
            time.sleep(2)
    
    goless.go(func2)

    while True:
        _, val = goless.select([goless.rcase(c1), goless.rcase(c2)])
        print(val)

if __name__ == "__main__":
    main()

```