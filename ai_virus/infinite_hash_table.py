"""
This module contains Infinite hash table
"""

from __future__ import annotations
from typing import Generic, TypeVar, List
from algorithms.mergesort import mergesort
from data_structures.referential_array import ArrayR

__author__ = "Adrian Ong Zhe Yee, Teh Yee Hong"

K = TypeVar("K")
V = TypeVar("V")


class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self, level: int = 0) -> None:
        self.array: ArrayR[tuple[K, V] | None] = ArrayR(self.TABLE_SIZE)
        self.count = 0
        self.level = level

    def hash(self, key: K) -> int:
        """
        Hash a key for insert/retrieve/update into the hashtable.

        :complexity: O(1)
        """
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE - 1)
        return self.TABLE_SIZE - 1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        param arg1: the key to get the value

        Returns: the value of the key

        :raises KeyError: when the key doesn't exist.

        Complexity: Best case occur when the item is straight away at the position (the position is not an InfiniteHashTable)
                    Complexity is O(1)
                    Worst case occur when the item is inside a lot of InfiniteHashTable, recursion occur a lot of time
                    Complexity is O(n)
        """

        def find_key(table, key):
            """
            To find the key

            param arg1: The table to be search
            param arg2: Used to get the position

            Returns: the value of the key

            :raises KeyError: when the key doesn't exist.

            Complexity: Best case occur when the item is straight away at the position (the position is not an InfiniteHashTable)
                        Complexity is O(1)
                        Worst case occur when the item is inside a lot of InfiniteHashTable, recursion occur a lot of time
                        Complexity is O(n)
            """
            position = self.hash(key)
            if table[position] is None:
                raise KeyError
            else:
                if isinstance(table[position], InfiniteHashTable):
                    self.level += 1
                    return find_key(table[position].array, key)
                else:
                    return table[position][1]

        self.level = 0
        return find_key(self.array, key)

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        param arg1: the key to find a spot
        param arg2: the value of the key

        Complexity: Best case occur when the first position is None, can be added straight away, Complexity is O(1)
                    Worst case occur when recursion occurs alot of time, Complexity is O(n)
        """

        def insert_key_value(table, key, value):
            """
            To find position to be added, if there's already a key in the position, and it's not an InfiniteHashTable,
            Create one and add both the old key and value and the current key and value into it

            param arg1: the table to be gone through
            param arg2: used to get the position
            param arg3: value to be added

            Complexity: Best case occur when the first position is None, can be added straight away, Complexity is O(1)
                        Worst case occur when recursion occurs alot of time, Complexity is O(n)
            """
            position = self.hash(key)
            if table[position] is None:
                table[position] = (key, value)
            else:
                if isinstance(table[position], InfiniteHashTable):
                    self.level += 1
                    insert_key_value(table[position].array, key, value)
                else:  # if it's a key-value pair
                    temp = InfiniteHashTable()
                    temp.level += self.level + 1
                    old_key = table[position][0]
                    old_value = table[position][1]
                    old_position = temp.hash(old_key)
                    table[position] = temp
                    temp.array[old_position] = (old_key, old_value)
                    self.level += 1
                    insert_key_value(temp.array, key, value)

        self.level = 0
        insert_key_value(self.array, key, value)

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table. How it works is by removing the key to be deleted,
        then get all the keys that share the same position with the key to be deleted, removing all of them out and
        adding them back again

        :raises KeyError: when the key doesn't exist.

        param arg1: the key to be deleted

        Complexity: Best case occur when the key cannot be found, Complexity is O(1)
                    Worst case occur when there's a lot of nested InfiniteHashTable for delete, then insert_remaining is needed,
                    then len(lst) != 0, Complexity is O(n) + O(1) + O(n * m) + O(n) = O(n * m)
        """

        def delete(table, key):
            """
            This function deletes the key and value pair

            param arg1: the table to be searched through
            param arg2: the key to be deleted

            complexity: Best case occur when the first position is already the key (not InfiniteHashTable),
                        Complexity is O(1)
                        Worst case occur when there is alot of InfiniteHashTable
                        Complexity is O(1)
            """
            position = self.hash(key)
            if isinstance(table[position], InfiniteHashTable):
                self.level += 1
                delete(table[position].array, key)
            else:
                table[position] = None
                return

        def reinsert_remaining(lst, table):
            """
            This function search for all the other values in the same position as the key to be deleted,
            then add them into a list

            param arg1: the list that contains the pairs
            param arg2: the table to be searched through

            complexity: Best case occur when every element in the table is None, no adding or recursion needed,
                        Complexity is O(n)
                        Worst case occur when there is a lot of nested InfiniteHashTable, recursion is needed,
                        Complexity is O(n * m), n is the loop and m is depth of InfiniteHashTable
            """
            for x in table:
                if x is not None:
                    if isinstance(x, InfiniteHashTable):
                        reinsert_remaining(lst, x.array)
                    else:
                        lst.append(x)

        if self.__contains__(key):
            self.level = 0
            delete(self.array, key)
        else:
            raise KeyError

        self.level = 0
        lst = []
        position = self.hash(key)
        if self.array[position] is not None:
            reinsert_remaining(lst, self.array[position].array)
            self.array[position] = None
            if len(lst) != 0:
                for x in lst:
                    self[x[0]] = x[1]

    def __len__(self) -> int:
        """
        Return the number of elements in the table

        Complexity: Best case occur when there's nothing in the table, hence looping only once, Complexity is O(n)
                    Worst case occur when there's alot of nested InfiniteHashTables, Complexity is O(n * m), n is the loop and m is depth of InfiniteHashTable
        """
        def count_elements(table):
            """
            This counts the number of elements in the table

            param arg1: the table to be searched through

            Returns: integer value of numbers of elements

            Complexity: Best case occur when there's nothing in the table, hence looping only once, Complexity is O(n)
                        Worst case occur when there's alot of nested InfiniteHashTables, Complexity is O(n * m), n is the loop and m is depth of InfiniteHashTable
            """
            count = 0
            for x in table:
                if isinstance(x, InfiniteHashTable):
                    count += count_elements(x.array)
                elif isinstance(x, tuple):
                    count += 1
            return count

        self.level = 0
        return count_elements(self.array)

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        pass

    def get_location(self, key) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.

        param arg1: the key to be found

        Returns: a list of integers

        Complexity: Best case occur when best case for find_position occur, Complexity is O(n)
                    Worst case occur when worst case for find_position occur, Complexity is O(n^2)
        """

        def find_position(lst, table, key):
            """
            this function search through InfiniteHashTables to get the sequence of positions

            param arg1: the list that stores the sequence
            param arg2: the table to be searched through
            param arg3: the key to be found

            Returns: the list containing sequence

            Complexity: Best case occur when there's no InfiniteHashTable, only key-value pair, Complexity is O(1)
                        Worst case occur when there's alot of nested InfiniteHashTable, Complexity is O(n)
            """
            position = self.hash(key)
            if table[position] is None:
                return lst
            else:
                lst.append(position)
                self.level += 1
                if isinstance(table[position], InfiniteHashTable):
                    return find_position(lst, table[position].array, key)
                else:
                    return lst

        if self.__contains__(key):
            self.level = 0
            lst = []
            find_position(lst, self.array, key)
            return lst
        else:
            raise KeyError

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        param arg1: the key to be found

        Returns: boolean

        Complexity: Best case occur when the position is None, Complexity is O(1)
                    Worst case occur when there are alot of nested InfiniteHashTable, Complexity is O(n)

        """

        def search(table, key):
            """
            This function helps to find the key

            param arg1: the table to be searched through
            param arg2: the key to be found

            Returns: boolean

            Complexity: Best case occur when the position is None, Complexity is O(1)
                        Worst case occur when there are alot of nested InfiniteHashTable, Complexity is O(n)
            """
            position = self.hash(key)
            if table[position] is None:
                return False
            else:
                if isinstance(table[position], InfiniteHashTable):
                    self.level += 1
                    return search(table[position].array, key)
                elif table[position][0] == key:
                    return True
            return False

        self.level = 0
        return search(self.array, key)

    def sort_keys(self, current=None) -> List[str]:
        """
        Returns all keys currently in the table in lexicographically sorted order.

        Param:
            current

        Return:
            A list of keys in lexicographically sorted order.

        Complexity:
            Best:
                O(n log n) where n is the total number of keys in the table.
                This occurs when the table is already sorted.

            Worst:
                O(n log n) where n is the total number of keys in the table.
                This occurs when the table is completely unsorted, and each merge step
                takes O(n) time.
        """
        keys = []

        for item in self.array:
            if isinstance(item, InfiniteHashTable):
                keys.extend(item.sort_keys())
            elif item:
                keys.append(item[0])
        return mergesort(keys)


if __name__ == '__main__':
    pass