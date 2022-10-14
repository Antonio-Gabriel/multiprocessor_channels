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
