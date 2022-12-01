from TreeParityMachine import TreeParityMachine
try:
    from ulab import numpy as np
    import urandom as random
except ImportError:
    import numpy as np
    import random


def StartTpmTest(k,n,l,learnRule,maxIterations):
    try:
        A = TreeParityMachine(k,n,l)
    except MemoryError:
        print("401")
    initialStimulus = np.array([[random.randrange(-1,2,2) for n in range(n)] for k in range(k)], dtype=np.int8) #Using the same stimulus vector for both trees
    stimulus = initialStimulus
    
    i = 0
    while i < maxIterations:
        try:
            print("201")
            A.setStimulus(stimulus)
            A.getResult()
            print("211")
        except MemoryError:
            print("401")
        try:
            print("202")
            A.learn(learnRule)
            print("212")
        except MemoryError:
            print("401")

        i += 1

    print("300") #finished

print("100") #100 is initialization
print("----------------------------")