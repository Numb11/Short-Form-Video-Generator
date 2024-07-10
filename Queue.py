class Queue:
    def __init__(self,length):
        self.frontpointer = -1
        self.rearpointer = 0
        self.length = length
        self.queue = []
        for i in range(length): (self.queue).append(None)
    def is_empty(self):
        return self.frontpointer == -1

    def is_full(self):
        return (self.rearpointer == self.length)

    def dequeue(self): #shuffle method removes frist element then shuffles other items down a place in the array(queue)
        if self.rearpointer == 0:
            self.frontpointer = -1
        if not(self.is_empty()):
            for i in range(len(self.queue)):
                if i == 0:
                    self.queue[i] = self.queue[1]
                else:
                    self.queue[i-1] = self.queue[i]
                self.queue[-1] = None
                self.rearpointer = self.rearpointer - 1
        
    def enqueue(self,item):
        if not(self.is_full()):
            if self.rearpointer == 0:
                self.frontpointer = self.frontpointer +1
                self.queue[self.rearpointer] = item
        else:
            self.queue[self.rearpointer] = item
            self.rearpointer = self.rearpointer +1
    def getqueue(self):
        return self.queue
