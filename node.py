class Node(object):
    '''Node class which is used for building the huffman tree'''
    
    def __init__(self, character, weight, left=None, right=None):
        '''Set the character, weight, left, and right of each node'''
        
        self.char = character
        self.weight = weight
        self.left = left
        self.right = right
    
    def __cmp__(self, sec_node):
        '''Return 1 if node self is greater than node sec_node, 
        -1 otherwise'''
        
        if (self.weight > sec_node.weight) or (self.weight == sec_node.weight\
                                               and self.char > sec_node.char):
            return 1
        else:
            return -1
        
    def __repr__(self):
        '''Return a human readable version of the node'''
        
        return repr((self.char, self.weight))
        
    def greater_character(self, sec_node):
        '''Return the greater character from node self and node sec_node'''
        
        return max(self.char, sec_node.char)
    
    def is_leaf(self):
        '''Return True if the Node self is a leaf, False otherwise.'''
        
        return not (isinstance(self.right, Node) or\
                    isinstance(self.left, Node))
