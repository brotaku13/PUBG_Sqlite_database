import time
import subprocess as sub
import sys

def loop(number):
    try:
        res = sub.run(["python", "input.py", str(number)], timeout=1)
    except sub.TimeoutExpired:
        loop(str(int(number) - 1))
        return
    return

def main():
    if len(sys.argv) != 2:
        print("Usage: python countdown.py int")
        return

    number = sys.argv[1]
    print("Press ENTER to go into testing mode.")
    loop(str(int(number)))
    return

if __name__ == "__main__":
    main()