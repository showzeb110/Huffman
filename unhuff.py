import tkFileDialog
from node import *
from huff import *
import BitVector
import sys

class FileNotCompressedError(Exception):
    '''Exception raised when the file selected is not a compressed 
    file(non-huffed file)'''
    
    pass

def read_bits(compressed_file):
    '''Return the str bit sequence from the given file name compressed_file'''
    
    bv = BitVector.BitVector(filename=compressed_file)
    str_bv = str(bv.read_bits_from_file(1024))
    while bv.more_to_read:
        str_bv += str(bv.read_bits_from_file(1024))
    return str_bv

def decode_compressed_file(bit_sequence, huffman_tree):
    '''Return a str message that is contained in the str bit_sequence using 
    the node huffman_tree'''
    
    return find_leaf(bit_sequence, huffman_tree, huffman_tree)

def find_leaf(bit_sequence, tree_node, tree_root):
    '''Return the characters of a leaf node tree_node from the node tree_root
    following the str bit_sequence'''
    
    #Base Case: if the tree_node is a leaf and the character is ''
    if tree_node.is_leaf():
        if tree_node.char == '':
            return tree_node.char
        #Recursive Case: if the character is not the eof characyer 
        else:
            return tree_node.char + find_leaf(bit_sequence, tree_root,\
                                         tree_root)
    #Recursive Case: if tree_node is not a leaf
    else:
        if bit_sequence != '':
            if bit_sequence[0] == '0':
                return find_leaf(bit_sequence[1:], tree_node.left, tree_root)
            else:
                return find_leaf(bit_sequence[1:], tree_node.right, tree_root)
        else:
            raise FileNotCompressedError("Error: File selected is not " +\
                                         "compressed")
    
if __name__ == "__main__":
    
    compressed_file_name = tkFileDialog.askopenfilename(title="Choose compress file to decompress")
    if not compressed_file_name:
        sys.exit("No File Selected to unhuff")
    uncompressed_file_name = tkFileDialog.asksaveasfilename(title="Choose compress file to decompress")
    if not uncompressed_file_name:
        sys.exit("No file selected to save the uncompressed file")
    char_frequency_file = open("char_freqs.txt")
    char_dict = eval(char_frequency_file.read())
    char_frequency_file.close()
    huffman_tree = make_huffman_tree(char_dict)
    bit_sequence = read_bits(compressed_file_name)
    uncompressed_file = open(uncompressed_file_name, 'w')
    uncompressed_file.write(decode_compressed_file(bit_sequence, huffman_tree))
    uncompressed_file.close()
