#!/usr/bin/python -B

'''
Created on Jul 14, 2013

@author: Bill Dimmick <me@billdimmick.com>
'''
import unittest
from heap import Heap, minheap, maxheap

DEFAULT_VALUES = [3,1,5,2,6,4]

class TestHeap(unittest.TestCase):
    def setUp(self):
        self.heap = None
        self.vals = None

    def makeHeap(self, values=DEFAULT_VALUES, comp = maxheap):        
        self.heap = Heap(comp)        
        self.vals = []    
        for val in values:
            self.heap.append(val)
            self.vals.append(val)  

    '''
    Test default max-heap and ensure None comes out when empty
    '''        
    def test_Empty(self):
        self.makeHeap([])
        self.assertEqual(None, self.heap.pop(), "Empty heap was not empty")
        self.assertEqual(0, len(self.heap), "Empty heap was not length 0")

    '''
    Test default max-heap and ensure a single values comes out
    '''        
    def test_SingleValue(self):
        self.makeHeap([1])
        self.assertEqual(1, len(self.heap), "Expected heap length was not 1")
        self.assertEqual(1, self.heap.pop(), "Single value heap returned no value!")
        self.assertEqual(0, len(self.heap), "Expected post-pop heap length was not 0")
        
    '''
    Test default max-heap and ensure the values come out in the expected order
    '''        
    def test_MutlipleValues(self):
        self.makeHeap()
        self.vals.sort()        
        oldval = 7
        while len(self.vals) > 0:
            self.assertEquals(len(self.vals), len(self.heap), "Expected heap length did not match %s" % len(self.vals))
            val = self.vals.pop()
            self.assertTrue(oldval > val)
            got = self.heap.pop()
            self.assertEquals(val, got, "Heap did not pop expected value %s, got %s" % (val, got))
            self.assertEquals(len(self.vals), len(self.heap), "Expected post-pop heap length did not match %s" % len(self.vals))
            oldval = val

    '''
    Test a custom min-heap and ensure the values come out in the expected order
    '''
    def test_MutlipleValuesCustomComparator(self):
        self.makeHeap(comp = minheap)
        self.vals.sort(reverse = True)
        oldval = 0        
        while len(self.vals) > 0:
            self.assertEquals(len(self.vals), len(self.heap), "Expected heap length did not match %s" % len(self.vals))
            val = self.vals.pop()
            self.assertTrue(oldval < val)
            got = self.heap.pop()
            self.assertEquals(val, got, "Heap did not pop expected value %s, got %s" % (val, got))
            self.assertEquals(len(self.vals), len(self.heap), "Expected post-pop heap length did not match %s" % len(self.vals))
            oldval = val 

    '''
    Test default max-heap and ensure one heap can be added to another for a whole new heap
    '''        
    def test_AdditionOfHeap(self):        
        self.makeHeap([3])
        heap2 = Heap()
        heap2.append(5)
        heapjoin = self.heap + heap2
        self.assertEquals(3, self.heap.pop())
        self.assertEquals(0, len(self.heap))
        self.assertEquals(5, heap2.pop())
        self.assertEquals(0, len(heap2))
        self.assertEquals(5, heapjoin.pop())
        self.assertEquals(3, heapjoin.pop())
        self.assertEquals(0, len(heapjoin))

    '''
    Test default max-heap and ensure one heap can be added to a seq for a whole new heap
    '''        
    def test_AdditionOfSeq(self):        
        self.makeHeap([3])        
        heapjoin = self.heap + [5]
        self.assertEquals(3, self.heap.pop())
        self.assertEquals(0, len(self.heap))
        self.assertEquals(5, heapjoin.pop())
        self.assertEquals(3, heapjoin.pop())
        self.assertEquals(0, len(heapjoin))

    '''
    Test default max-heap and ensure one heap can be added to an obj for a whole new heap
    '''        
    def test_AdditionOfObj(self):        
        self.makeHeap([3])
        heapjoin = self.heap + 5
        self.assertEquals(3, self.heap.pop())
        self.assertEquals(0, len(self.heap))
        self.assertEquals(5, heapjoin.pop())
        self.assertEquals(3, heapjoin.pop())
        self.assertEquals(0, len(heapjoin))

    '''
    Test default max-heap and ensure one heap can be appended to another and only modify one
    '''                    
    def test_SelfAddOfHeap(self):
        self.makeHeap([3])        
        heap2 = Heap()
        heap2.append(5)
        self.heap += heap2
        self.assertEquals(5, heap2.pop())
        self.assertEquals(0, len(heap2))        
        self.assertEquals(5, self.heap.pop())
        self.assertEquals(3, self.heap.pop())
        self.assertEquals(0, len(self.heap))

    '''
    Test default max-heap and ensure one heap can have a seq appended to it and only modify the heap
    '''                    
    def test_SelfAddOfSeq(self):
        self.makeHeap([3])        
        self.heap += [5]        
        self.assertEquals(5, self.heap.pop())
        self.assertEquals(3, self.heap.pop())
        self.assertEquals(0, len(self.heap))

    '''
    Test default max-heap and ensure one heap can have an object appended to it and only modify the heap
    '''                    
    def test_SelfAddOfObj(self):
        self.makeHeap([3])
        self.heap += 5
        self.assertEquals(5, self.heap.pop())
        self.assertEquals(3, self.heap.pop())
        self.assertEquals(0, len(self.heap))
        
    '''
    Test default drain and ensure the values come out in the expected order
    '''        
    def test_SimpleDrain(self):
        self.makeHeap()
        self.assertEquals([6,5,4,3,2,1], self.heap.drain())

    '''
    Test filtered drain and ensure the values come out in the expected order
    '''        
    def test_FilterDrain(self):
        self.makeHeap()
        self.assertEquals([6,4,2], self.heap.drain(filt = lambda a: a % 2 == 0))

    '''
    Test drain-until and ensure the values come out in the expected order
    '''        
    def test_DrainUntil(self):
        self.makeHeap()
        drained = self.heap.drain(until = lambda a: a > 3)
        self.assertEquals([6,5,4], drained)
        self.assertEquals(3, self.heap.pop())

    '''
    Test drain-until with a filter and ensure the values come out in the expected order
    '''        
    def test_DrainUntilWithFilter(self):
        self.makeHeap()
        drained = self.heap.drain(lambda a: a > 3, lambda a: a % 2 == 0)
        self.assertEquals([6,4], drained)
        self.assertEquals(5, self.heap.pop())

    '''
    Test contains functionality
    '''
    def test_Contains(self):
        self.makeHeap()
        self.assertTrue(6 in DEFAULT_VALUES)
        self.assertTrue(1 in DEFAULT_VALUES)
        self.assertTrue(6 in self.heap)
        self.assertTrue(1 in self.heap)
        self.heap.pop()        
        self.assertFalse(6 in self.heap)
        self.assertTrue(6 not in self.heap)
        self.assertTrue(1 in self.heap)
        
        
if __name__ == '__main__':
    unittest.main()