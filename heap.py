#!/usr/bin/python -B

'''
Created on Jul 14, 2013

@author: Bill Dimmick <me@billdimmick.com>
'''

'''
Functional comparitor for minimal heap building
'''
def minheap(a, b):
    return a < b


'''
Functional comparitor for maximal heap building
'''
def maxheap(a, b):
    return a > b
    

class Heap(object):
    def __init__(self, comp=maxheap):
        self.values=[]
        self.comparator = comp
        
    def __parent__(self, i):
        return i // 2
    
    def __left__(self, i):
        return (i * 2) + 1
    
    def __right__(self, i):
        return (i + 1) * 2
        
    def __add__(self, other):
        result = Heap()
        result.values.extend(self.values)
        result+=other
        return result
    
    def __contains__(self, i):
        return i in self.values
    
    def __heapify__(self, i):
        left = self.__left__(i)
        right = self.__right__(i)
        bound = len(self.values)
        largest = i
        if (left < bound) and (self.comparator(self.values[left], self.values[largest])):
            largest = left
        if (right < bound) and (self.comparator(self.values[right], self.values[largest])):
            largest = right
        if largest is not i:
            self.__swap__(i, largest)
            self.__heapify__(largest)

    def __iadd__(self, other):
        if type(other)==Heap:
            for val in other.values:
                self.append(val)
        elif '__iter__' in dir(other):            
            for val in other:
                self.append(val)
        else:
            self.append(other)
        return self

    def __len__(self):
        return len(self.values)

    def __swap__(self, i, j):
        v = self.values[i]
        self.values[i] = self.values[j]
        self.values[j] = v
            
    def append(self, obj):
        self.values.append(obj)
        i = len(self.values) - 1
        parent = self.__parent__(i)
        while (i > 0) and (self.comparator(self.values[i], self.values[parent])):
            self.__swap__(i, parent)
            i = parent
            parent = self.__parent__(i)

    def drain(self, until = None, filt = None):
        result = []
                
        if until:
            skipped = []
            while (until(self.values[0])):
                val = self.pop()
                if filt:
                    if (filt(val)):
                        result.append(val)
                    else:
                        skipped.append(val)
                else:
                    result.append(val)
            for k in skipped:
                self.append(k)
        else:
            if not filt:
                filt = lambda a: True
            while len(self.values) > 0:
                val = self.pop()
                if filt(val):
                    result.append(val)
        return result
        
    def pop(self):
        if (len(self.values) > 0):
            result = self.values[0]
            end = len(self.values) - 1
            self.values[0] = self.values[end]
            self.values = self.values[0:end]
            self.__heapify__(0)
            return result