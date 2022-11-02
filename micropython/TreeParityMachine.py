try:
    from ulab import numpy as np
    import urandom as random
except ImportError:
    import numpy as np
    import random


class TreeParityMachine:
    stimulus = np.zeros(1)
    weights = np.zeros(1)
    sigma = np.zeros(1)
    output = 0

    def __init__(self,k,n,l):
        self.K = k
        self.N = n
        self.L = l
        self.setRandomWeights()
    

#####
    def sign(self,r):
        if r > 0:
            return 1
        elif r == 0 or r < 0:
            return -1

    def localField(self, n, v, u):
        dotProd = np.dot(v,u)
        return dotProd/np.sqrt(n)

    def outputSigmaFunction(self,h):
        if h == 0:
            return -1
        else:
            return self.sign(h)

    def thauFunction(self,x):
        mul = 1
        for i in x:
            mul *= i
        return mul

    def heavisideStepFunction(self, x):
        if x > 0:
            return 1
        else:
            return 0

    def gFunction(self, x, l):
        if abs(x) > l:
            return self.sign(x) * l
        else:
            return x

    def hebbianLearningRule(self, thau, stA, wsA):
        # tA, tB are the outputs of TPM A and TPM B, respectively.
        # stA is the stimulus vector, and wsA is the weight vector of TPM A.
        localSigma = self.outputSigmaFunction(self.localField(self.N, stA, wsA))
        for i in range(len(wsA)):
            wsA[i] = self.gFunction(wsA[i] + stA[i] * thau * self.heavisideStepFunction(localSigma * thau) * self.heavisideStepFunction(thau * thau), self.L)
        return wsA

    def antiHebbianLearningRule(self, thau, stA, wsA):
        # tA, tB are the outputs of TPM A and TPM B, respectively.
        # stA is the stimulus vector, and wsA is the weight vector of TPM A.
        localSigma = self.outputSigmaFunction(self.localField(self.N, stA, wsA))
        for i in range(len(wsA)):
            wsA[i] = self.gFunction(wsA[i] - stA[i] * thau * self.heavisideStepFunction(localSigma * thau) * self.heavisideStepFunction(thau * thau), self.L)
        return wsA

    def randomWalkLearningRule(self, thau, stA, wsA):
        # tA, tB are the outputs of TPM A and TPM B, respectively.
        # stA is the stimulus vector, and wsA is the weight vector of TPM A.
        localSigma = self.outputSigmaFunction(self.localField(self.N, stA, wsA))
        for i in range(len(wsA)):
            wsA[i] = self.gFunction(wsA[i] + stA[i] * self.heavisideStepFunction(localSigma * thau) * self.heavisideStepFunction(thau * thau), self.L)
        return wsA

    learningRules = {0: hebbianLearningRule, 1: antiHebbianLearningRule, 2: randomWalkLearningRule}
    
####


    def setStimulus(self,v):
        self.stimulus = v

    def getWeights(self):
        return self.weights
    def setWeights(self,w):
        self.weights = w
    def setRandomWeights(self):
        newWeights = np.array([[random.randint(-self.L,self.L) for n in range(self.N)] for k in range(self.K)], dtype=np.int8)
        self.weights = newWeights

    def getResult(self):
        self.sigma = np.array([self.outputSigmaFunction(self.localField(self.N,self.stimulus[i],self.weights[i])) for i in range(self.K)], dtype=np.int8)
        self.output = self.thauFunction(self.sigma)
        return self.output

    def learn(self,learningRuleIndex):
        for i in range(self.K):
            self.weights[i] = self.learningRules[learningRuleIndex](self,self.output,self.stimulus[i],self.weights[i])