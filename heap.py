'''This heap.py is from anya's week 9 lecture notes,
But I did modify some parts of her code.

Modifications/Changes
- add __len__(self) function
- change __str__{self} --> __repr__(self) function
- add bubble_up(heap, i) function #Uses Recursion
  the original code uses a while loop to bubble up
- add bubble_down(heap, i) function #Uses Recursion
  the original code uses a while loop to bubble down
- delete build_heap(L) function
- delete the if __name__ == "__main__": block
'''

class EmptyHeapError(Exception):
    '''Raise an exception when the heap is empty'''
    
    pass

class Heap(object):
    """An implementation of a Min-Heap ADT."""

    def __init__(self):
        '''Create an empty Min-Heap.'''

        self.data = []
        
    def __len__(self):
        '''Return the length of the heap'''

        return len(self.data)
    
    def __repr__(self):
        '''Return the human readable representation of the data
        in this heap.'''

        return repr(self.data)
    
    def is_empty(self):
        '''Return whether this heap is empty.'''

        return not self.data
    
    def add(self, item):
        '''Put a new data item in the heap.'''

        self.data.append(item)
        bubble_up(self, len(self.data) - 1)
    
    def pop_root(self):
        '''Remove and the return the root of this heap.
        Raises EmptyHeapError if this heap is empty.'''

        if self.is_empty():
            raise EmptyHeapError("Error: The Heap is empty")
        
        root = self.data[0]
        last_data = self.data.pop()
        if not self.data:
            return root
        self.data[0] = last_data
        bubble_down(self, 0)
        return root

    def _exists(self, i):
        '''Return whether there is a node at index i in this heap.'''

        return i < len(self.data)
    
    def _smaller_child(self, i):
        '''Return the index of the smaller of the children of the node
        and index i, or None if the node at index i has no children.'''

        left, right = _left_child(i), _right_child(i) 
        if not self._exists(left):
            return None
        if not self._exists(right):
            return left
        if self.data[left] < self.data[right]:
            return left
        else:
            return right

def bubble_up(heap, i):
    '''Bubble up the item at index i of the Heap heap, swapping with each
    parent until heap.data is heapified (min heap).'''
    
    #Recursive Case: if the child is less than the parent, bubble up
    if (i > 0) and (heap.data[i] < heap.data[_parent(i)]):
        heap.data[i], heap.data[_parent(i)] = \
                          heap.data[_parent(i)], heap.data[i]
        bubble_up(heap, _parent(i))
    #Base Case: if the child is bigger than the parent, do nothing        
        
def bubble_down(heap, i):
    '''Bubble down the item at index i of the Heap heap, swapping with
    each smaller_child until heap.data is heapified (min heap).'''
    
    #Recursive Case: if the parent is greater than smaller_child, bubble down
    smaller_child = heap._smaller_child(i)
    if smaller_child and (heap.data[smaller_child] < heap.data[i]):
        heap.data[i], heap.data[smaller_child] =\
                 heap.data[smaller_child], heap.data[i]
        bubble_down(heap, smaller_child)
    #Base Case: if parent is less than smaller_child, do nothing
        
def _parent(i):
    '''Return the index of the parent node of the node at index i.'''

    return (i - 1) / 2

def _left_child(i):
    '''Return the index of the left child of the node at index i.'''

    return 2 * i + 1

def _right_child(i):
    '''Return the index of the right child of the node at index i.'''

    return 2 * i + 2
