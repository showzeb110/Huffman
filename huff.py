import tkFileDialog
from heap import *
from node import *
import sys
import BitVector

def freq_table(text, output_file):
    '''Return a dictionary that contains the characters in str text as keys
    and the number of times it appears in str text as values.
    Save the dictionary in a file output_file'''
    
    char_dict = {}
    for char in text:
        if char in char_dict:
            char_dict[char] += 1
        else:
            char_dict[char] = 1
    output_file.write(repr(char_dict))
    return char_dict

def make_huffman_tree(char_dict):
    '''Make a huffman tree based on char_dict'''
    
    forest = Heap()
    for key in char_dict:
        forest.add(Node(key, char_dict[key]))
    #Manually add the psuedo eof character in the forest
    forest.add(Node('', 1))
    while len(forest) != 1:
        smallest = forest.pop_root()
        second_smallest = forest.pop_root()
        #Make a new node
        new_char = Node.greater_character(smallest, second_smallest)
        new_weight = smallest.weight + second_smallest.weight
        new_node = Node(new_char, new_weight, second_smallest, smallest)
        forest.add(new_node)
    return forest.pop_root()
    
def make_binary_code(char_dict, huffman_tree):
    '''Return a dictionary with characters as keys(that is based on dict 
    char_dict) and their binary code as their values(that is based on the 
    Node huffman_tree)'''

    binary_dict = {}
    for key in char_dict:
        binary_dict[key] = find_root_to_leaf_path(key, huffman_tree)
    #Manually add the psuedo eof character in the binary_dict
    binary_dict[''] = find_root_to_leaf_path('', huffman_tree)
    return binary_dict

def find_root_to_leaf_path(key, huffman_tree):
    '''Return an str which is a sequence of 0's and 1's which represents the 
    binary code(which will be based on root to leaf path of the huffman tree 
    0-left, 1-right ) for char key.'''
    
    path = ""
    #Base Case if the node is a leaf
    if (huffman_tree.is_leaf()): #This means that the tree has only one node
        if huffman_tree.char == key:
            return ""
        else:
            return "2"
    #Recursive Case: if the node is not a leaf
    else:
        if huffman_tree.left:
            path = "0" + find_root_to_leaf_path(key, huffman_tree.left)
            if ("2" not in path): #then it is a valid path
                return path
        if huffman_tree.right:
            path = "1" + str(find_root_to_leaf_path(key, huffman_tree.right))
            if ("2" not in path): #then it is a valid path
                return path
        return "2"

def write_bit_sequence(text, binary_dict):
    '''Return a str binary sequence of the str text based on the given 
    dict binary_dict'''
    
    binary_sequence = ""
    for char in text:
        binary_sequence += binary_dict[char]
    #Manually add the psuedo eof character at the end of the bit_sequence
    binary_sequence += binary_dict['']
    return binary_sequence

def build_bit_vector(bit_sequence):
    '''Return a BitVector from the given str bit_sequence'''
    
    bv = BitVector.BitVector(bitstring=bit_sequence)
    if (len(bit_sequence) % 8) is not 0:
        padding = 8 - (len(bit_sequence) % 8)
        bv = BitVector.BitVector._resize_pad_from_right(bv, padding)
    return bv

if __name__ == "__main__":
    
    input_file_name = tkFileDialog.askopenfilename(title="Choose file to Compress")
    if not input_file_name:
        sys.exit("No file selected to be compressed")
    compressed_file_name = tkFileDialog.asksaveasfilename(title="Type name to save file as")
    if not compressed_file_name:
        sys.exit("No file selected to save the compressed file")
    input_file = open(input_file_name)
    contents = input_file.read()
    input_file.close()
    output_file = open("char_freqs.txt", "w")
    char_dict = freq_table(contents, output_file)
    output_file.close()
    huffman_tree = make_huffman_tree(char_dict)
    binary_dict = make_binary_code(char_dict, huffman_tree)
    bit_sequence = write_bit_sequence(contents, binary_dict)
    bv = build_bit_vector(bit_sequence)
    compressed_file = open(compressed_file_name, 'wb')
    bv.write_to_file(compressed_file)
    compressed_file.close()
