import multiprocessing as mp
import time
import random
import sys

def func_A(process_number, queue, proceed):
    print ("Process {} has started been created".format(process_number))

    print ("Process {} has ended step A".format(process_number))
    sys.stdout.flush()
    queue.put((process_number, "done"))

    proceed.wait() #wait for the signal to do the second part
    print ("Process {} has ended step B".format(process_number))
    sys.stdout.flush()

def multiproc_master():
    queue = mp.Queue()
    proceed = mp.Event()

    processes = [mp.Process(target=func_A, args=(x, queue, proceed)) for x in range(4)]
    for p in processes:
        p.start()

    #block = True waits until there is something available
    results = [queue.get(block=True) for p in processes]
    proceed.set() #set continue-flag
    for p in processes: #wait for all to finish (also in windows)
        p.join()
    return results

if __name__ == '__main__':
    split_jobs = multiproc_master()
    print (split_jobs)