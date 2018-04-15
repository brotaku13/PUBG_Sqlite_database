import time
import subprocess as sub
import sys
def main():
    if len(sys.argv) != 2:
        print("Usage: python countdown.py int")
        return

    number = sys.argv[1]
    test = "exit"
    for i in range(int(number), 0, -1):
        if int(number) > 1:
            test = input(f"{i}...")
        elif int(number) == 1:
            print(f"{i}...")
            time.sleep(1)
            print('', end='', flush=True)
            return
        if test == '':
            return
        time.sleep(1)
if __name__ == "__main__":
    main()