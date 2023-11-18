from doubly_linked_list import DoublyLinkedList
from random import randint, choice
import numpy as np

class HashSet:
    PRIMES = (25165843, 50331653, 100663319, 201326611, 402653189)

    def __init__(self):
        """
            Description of Function:
                initializes an empty table
            Parameters:
                None
            Return:
                None
        """
        self._init_table(16)

    def _init_table(self, new_capacity):
        """
        Private Method:
            Description of Function:
                initializes an empty table and buckets
            Parameters:
                new_capacity: shape of the array
            Return:
                None
        """
        self.the_table = np.empty(new_capacity, dtype = DoublyLinkedList)
        self.prime = choice(HashSet.PRIMES)
        self.a = randint(1, self.prime - 1)
        self.b = randint(0, self.prime - 1)
        self.size = 0

        #creating the buckets
        for i in range(len(self.the_table)):
            self.the_table[i] = DoublyLinkedList()

    def _hash_and_compress(self, k):
        """
        Private Method:
            Description of Function:
                returns the index of the bucket where the v exists
            Parameters:
                k: the v
            Return:
                int
        """
        return (hash(k) * self.a + self.b) % self.prime % len(self.the_table)
    
    def _expand_table(self):
        """
        Private Method:
            Description of Function:
                expands the table geometrically
            Parameters:
                None
            Return:
                None
        """
        #store the items
        items = self.values()

        #expand the table
        self._init_table(len(self.the_table) * 2)

        #rehash the items into the new table
        for item in items:
            self.add(item)

    def __iter__(self):
        """
            Description of Function:
                creates an iterable over the keys
            Parameters:
                None
            Return:
                None
        """
        return iter(self.values())

    def __str__(self):
        """
            Description of Function: 
                returns a string representing the set
            Parameters: 
                None
            Return: 
                str
        """
        return str(self.values())

    def get_size(self):
        """
            Description of Function: 
                returns the size of the set
            Parameters: 
                None
            Return: 
                int
        """
        return self.size
    
    def is_empty(self):
        """
            Description of Function: 
                returns True if the table is empty, False otherwise
            Parameters: 
                None
            Return: 
                bool
        """
        return self.size == 0

    #iterable method
    def values(self):
        """
        Description of Function:
            creates an iterable over the values of the set
        Parameters:
            None
        Return:
            None
        """
        return [v for bucket in self.the_table for v in bucket]

    def output_table_info(self):
        """
        Description:
            outputs information about the table
        Parameters:
            None
        Return:
            None
        """
        max_bucket_size = 0

        for i in range(len(self.the_table)):
            print(f"{i}: {self.the_table[i]}")
            
            if self.the_table[i].size > max_bucket_size:
                max_bucket_size = self.the_table[i].size

        print("Size of largest bucket: ", max_bucket_size)
        print("Table size: ", self.size)
        print("Load factor: ", self.size / len(self.the_table))

    #* Implementation of the Set interface
    def contains(self, v) -> bool:
        """
        Description of Function:
            returns True if the set contains the value, False otherwise
        Parameters:
            v: the value to search for
        Return:
            bool
        """
        index = self._hash_and_compress(v)
        bucket = self.the_table[index]
        for item in bucket:
            if item == v:
                return True
        
        return False
    
    def add(self, v):
        """
        Description of Function:
            adds v to the set, if it isn't already present
        Parameters:
            v: the value being added
        Return:
            None
        """
        load_factor = self.size / len(self.the_table)

        if load_factor > 0.75:
            self._expand_table()

        if not self.contains(v):
            index = self._hash_and_compress(v)
            self.the_table[index].add_first(v)
            self.size += 1
        
        return None

    def discard(self, v):
        """
        Description of Function:
            removes v from the set 
        Parameters:
            v: the value being removed
        Return:
            None
        """
        if self.contains(v):
            index = self._hash_and_compress(v)
            self.the_table[index].remove_value(v)
            self.size -= 1
        
        return None
    
    #Set Operations
    def union(self, other):
        """
        Description of Function:
            returns a new set of items found in the both sets
        Parameters:
            other: the other set
        Return:
            HashSet Object
        """
        result = HashSet()

        for element in self:
            result.add(element)
        for element in other:
            result.add(element)

        return result

    def intersection(self, other):
        """
        Description of Function:
            returns a new set of items found in both self and other
        Parameters:
            other: the other set
        Return:
            HashSet Object
        """
        result = HashSet()

        for element in self:
            if other.contains(element):
                result.add(element)

        return result

    def difference(self, other):
        """
        Description of Function:
            returns a new set of items found in self and not in other
        Parameters:
            other: the other set
        Return:
            HashSet Object
        """
        result = HashSet()

        for element in self:
            if other.contains(element) == False:
                result.add(element)

        return result

def test_set():
    setA = HashSet()

    setA.add(6)
    setA.add(2)
    setA.add(3)
    setA.add(4)

    setB = HashSet()

    setB.add(8)
    setB.add(2)
    setB.add(3)
    setB.add(7)

    setC = HashSet()
    
    setC.add(9)
    setC.add(2)
    setC.add(3)
    setC.add(4)

    setD = HashSet()

    setD.add(1)
    setD.add(2)
    setD.add(3)
    setD.add(4)

    setA = setA.union(setB)
    print(setA)

    setA = setA.difference(setB)
    print(setA)

    setB = setB.intersection(setC)
    print(setB)

test_set()

def algorithm(unsorted_list: list):
    """
    Description of Function:
        determines if there exist a x in the list such that 
        x and -x are in the list
    Parameters:
        unsorted_list: the unsorted list
    Return:
        bool
    """
    set = HashSet()

    for item in unsorted_list:
        set.add(item)

    for item in unsorted_list:
        inverse = item * -1

        if set.contains(inverse):
            return True
        
    return False

print(algorithm([1, 2, 3, -3, 5, 6,]))
