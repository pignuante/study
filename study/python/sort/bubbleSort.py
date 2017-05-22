import time

def bubbleSort(l):
    startTime=time.time()
    print("start   : {}".format( l))
    for s in range(len(l)-1):
        for e in range(len(l)-1, s, -1):
            if l[e] < l[e-1]:
                l[e],l[e-1] = l[e-1],l[e]
                print("changed : {}".format(l))
    print("result  : {}".format(l))
    print(time.time() - startTime)

