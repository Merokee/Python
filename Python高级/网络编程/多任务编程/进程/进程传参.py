import multiprocessing

def runProcess(*args, **kwargs):
    print(args)
    print(kwargs)

def main():
    p = multiprocessing.Process(target=runProcess, args=(1,2), kwargs={"hh":4, "ww":5})
    p.start()

if __name__ == "__main__":
    main()
