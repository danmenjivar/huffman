'''
Algorithms HW #2
Huffman
Based on: https://www.youtube.com/watch?v=nr3bZdL0aCs 

Prints each unique character (most to least frequent) alongside:
'''

print('Huffman Encoding Program')
file_name = input('Enter the name of a text file to open: ') + '.txt' #  prompt the user the name of a textfile

file = open(file_name, 'r') 
if file.mode == 'r':
    contents = file.read() # read the contents of that text file

letters = [] # make a list of characters with their corresponding frequencies (e.g. [3, 'g'])
only_letters = [] # and a list of only the characters used
for letter in contents: 
    if letter not in letters:
        freq = contents.count(letter)
        letters.append(freq)
        letters.append(letter)
        only_letters.append(letter)

temp_letters_with_frequency = list.copy(letters)
letters_with_frequency = []
# print(temp_letters_with_frequency) # this list is used to sort the codes
for i in range(0, len(temp_letters_with_frequency), 2):
    new_element_for_letters_freq = [temp_letters_with_frequency[i], temp_letters_with_frequency[i + 1]]
    letters_with_frequency.append(new_element_for_letters_freq)
letters_with_frequency.sort(key=lambda x : x[0], reverse=True)
# print(letters_with_frequency)

nodes = [] # generate the base nodes for the Huffman tree as "[freq, letter] => [7, "e"]"
while len(letters) > 0:
    nodes.append(letters[0:2])
    letters = letters[2:]
nodes.sort()
huffman_tree = []
huffman_tree.append(nodes) # add all the nodes to the tree

def combine(nodes): # recursively combine base nodes to create a huffman tree
    pos = 0
    newnode = []
    if len(nodes) > 1: # grab the 2 lowest nodes
        nodes.sort(key=lambda x : int(x[0]))
        nodes[pos].append('0') #  add a 0 or 1
        nodes[pos + 1].append('1')
        combined_node1 = str(nodes[pos][0]) + str(nodes[pos + 1][0])
        combined_node2 = str(nodes[pos][1]) + str(nodes[pos + 1][1])
        newnode.append(combined_node1)
        newnode.append(combined_node2)
        newnodes = []
        newnodes.append(newnode)
        newnodes = newnodes + nodes[2:]
        nodes = newnodes
        huffman_tree.append(nodes)
        combine(nodes)
    return huffman_tree

newnodes = combine(nodes)
huffman_tree.sort(key = lambda x: str(x[0]), reverse=True) #  invert the tree to match hand drawn
checklist = [] # remove any duplicates
for level in huffman_tree:
    for node in level:
        if node not in checklist:
            checklist.append(node)
        else:
            level.remove(node)
count = 0
# for level in huffman_tree: #print tree
#     print('Level', count, ':', level)
#     count += 1

# print()

letter_binary = []
if len(only_letters) == 1:
    letter_code = [only_letters[0], '0']
    letter_binary.append(letter_code * len(contents))
else: 
    for letter in only_letters:
        lettercode = ''
        for node in checklist:
            if len(node) > 2 and letter in node[1]:
                lettercode = lettercode + node[2]
        letter_code = [letter, lettercode]
        letter_binary.append(letter_code)

print(letters_with_frequency)
print(letter_binary)

print('Binary codes are: ')
print('Character\tBinary Huffman\tBinary ASCII')
for letter in letter_binary:
    print('\'%s\'\t\t%s\t\t%s' % (letter[0], letter[1], bin(ord(letter[0][0]))))

bitstring = '' #  create a bitstring of the original message using the created codes
for character in contents:
    for item in letter_binary:
        if character in item:
            bitstring = bitstring + item[1]

print("The contents of the file are: \'%s\'" % contents) # print the original content
print('The huffman encoded contents are: \'%s\'' % bitstring) # print the huffman coded content
