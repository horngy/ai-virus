"""
This module contains Double key table
"""

from __future__ import annotations
from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

__author__ = "Adrian Ong Zhe Yee, Teh Yee Hong"

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')


class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:
        if sizes is not None:
            self.TABLE_SIZES = sizes

        if internal_sizes is not None:
            self.internal_sizes = internal_sizes
        else:
            self.internal_sizes = self.TABLE_SIZES

        self.size_index = 0
        self.array: ArrayR[tuple[K1, V] | None] | None = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31417
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31417
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2 | None, is_insert: bool) -> tuple[int, int] | int:
        """
        Find the correct position for this key in the hash table using linear probing.

        Params:
            key1 (K1): The first key that use to find the position.
            key2 (K2 | None): The second key that use to find the position, can be None.
            is_insert (bool): To check whether the keys are being inserted or not.

        Returns:
            If key2 is not None, returns a tuple (position_key1, position_key2) indicating the positions for both keys.
            If key2 is None, returns the position for key1.

        Raises:
            KeyError: If the key pair is not in the table, but is_insert is False.
            FullError: If the table or sub-table is full and cannot insert the keys.

        Complexity:
            Best Case:
                O(hash1 + hash2), This occurs when both hash function (hash1 and hash2) are efficient,
                and the desired slots for both keys are immediately available without any collisions.
            Worst Case:
                O(hash1 + n + hash2 + m), This occurs when extensive linear probing is required
                for both keys, potentially involving scanning through n slots where n is the top-level table
                and m slots where m is the bottom-level table.
        """

        def key_insert_position(key1: K1, is_insert: bool) -> int:
            """
            Method used to find the position to insert key1

            Param:
                key1 (K1): The key that use to find the insert position.
                is_insert (bool): To check whether key1 is being inserted or not.

            Return:
                the correct position for key1 to insert in the array

            Raises:
                KeyError: When key1 is None in the table and is_insert is False
                FullError: If the top-level table is full.

            Complexity:
                Best case:
                    O(hash1 + comp==)
                    O(hash1) refers to the complexity of hash1 function
                    This occur only when we need to find the position of a key when in_insert is False
                    and no probing is needed

                Worst case:
                    O(hash1 + comp== + n), where n is the length of the table size
                    O(hash1) refers to the complexity of hash1 function
                    This occur when the position of key1 is occupied by other keys and had to search through
                    the entire table to find the last empty space to insert. This led to the complexity of O(n)
                    Hence, the overall time complexity for the worst case scenario is O(hash1 + n)
            """

            position_key = self.hash1(key1)
            for i in range(self.table_size):
                if self.array[position_key] is None:
                    if is_insert is not True:
                        raise KeyError(key1)
                    else:
                        sub_table = create_sub_table()
                        self.array[position_key] = (key1, sub_table)
                        return position_key
                elif self.array[position_key][0] == key1:
                    return position_key
                else:
                    position_key = (position_key + 1) % self.table_size
            raise FullError("Top-level table is full!")

        def create_sub_table():
            """
            Creates a new sub-table for the `_linear_probe` method.

            Returns:
                LinearProbeTable: A new instance of a sub-table used for linear probing.

            Note:
                This function is typically used internally by the `_linear_probe` method.

            Example:
                sub_table = create_sub_table()
            """
            sub_table = LinearProbeTable(self.internal_sizes)
            sub_table.hash = lambda k: self.hash2(k, sub_table)
            return sub_table

        key1_position = key_insert_position(key1, is_insert)

        if key2 is not None:
            sub_table = self.array[key1_position][1]
            key2_position = sub_table.hash(key2)

            for _ in range(sub_table.table_size):
                if sub_table.array[key2_position] is None:
                    if is_insert:
                        return key1_position, key2_position
                    else:
                        raise KeyError((key1, key2))
                elif sub_table.array[key2_position][0] == key2:
                    return key1_position, key2_position
                else:
                    key2_position = (key2_position + 1) % sub_table.table_size
            raise FullError("Sub-table is full!")
        else:
            return key1_position



    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        Returns an iterator of keys in the hash table.

        Params:
            key (K1 | None): If None, returns an iterator of all top-level keys in the hash table.
                             If not None, returns an iterator of all low-level keys in the sub-table of given top-level key.

        Returns:
            Iterator[K1 | K2]: An iterator of keys.

        Raises:
            None.

        Complexity:
            Best:
                - When key is None: O(1) this occurs when the first slot in the top-level hash table is not None.
                - When key is not None: O(1) this occurs when the desired key is found in the top-level hash table and
                                        its associated sub-table has at least one element.
            Worst:
                - When key is None: O(n) this occurs when none of the slots in the top-level hash table contain any elements.
                - When key is not None: O(m) this occurs when the desired key is not found in the top-level hash table, or its
                                        associated sub-table is empty.
        """
        if key is None:
            for i in range(self.table_size):
                if self.array[i] is not None:
                    yield self.array[i][0]
        else:
            try:
                position = self._linear_probe(key, None, False)
                if isinstance(position, tuple):
                    position = position[0]
                sub_table = self.array[position][1]
                for i in range(sub_table.table_size):
                    if sub_table.array[i] is not None:
                        yield sub_table.array[i][0]
            except KeyError:
                return None

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        Returns an iterator of values in the hash table.

        Params:
            key (K1 | None): If None, returns an iterator of all values in the entire double key hash table.
                             If not None, returns an iterator of all values in the sub-table of the given top-level key.

        Returns:
            Iterator[V]: An iterator of values.

        Raises:
            None.

        Complexity:
            Best:
                - When key is None: O(1) this occurs when the first slot in the top-level hash table contains a
                                    non-empty sub-table, and this sub-table has at least one element.
                - When key is not None: O(1) this occurs when the desired key is found in the top-level hash table and
                                        its associated sub-table has at least one element.
            Worst:
                - When key is None: O(n + m) this occurs when none of the slots in the top-level hash table contain any elements,
                                    or all associated sub-tables are empty.
                - When key is not None: O(m) this occurs when the desired key is not found in the top-level hash table,
                                        or its associated sub-table is empty.
        """
        if key is None:
            for i1 in range(self.table_size):
                if self.array[i1] is not None:
                    sub_table = self.array[i1][1]
                    for i2 in range(sub_table.table_size):
                        if sub_table.array[i2] is not None:
                            yield sub_table.array[i2][1]
        else:
            try:
                position = self._linear_probe(key, None, False)
                sub_table = self.array[position][1]
                for i in range(sub_table.table_size):
                    if sub_table.array[i] is not None:
                        yield sub_table.array[i][1]
            except KeyError:
                return None

    def keys(self, key: K1 | None = None) -> list[K1 | K2]:
        """
        Returns a list of keys in the hash table.

        Params:
            key (K1 | None): If None, returns all top-level keys in the hash table.
                             If not None, returns all bottom-level keys for the given top-level key.

        Returns:
            list[K1 | K2]: A list of keys.

        Raises:
            None.

        Complexity:
            Best:
                - When key is None: O(n) this occurs when the first slot in the top-level hash table is not None.
                - When key is not None: O(m) this occurs when the desired top-level key is found in the table and
                                        its associated sub-table has at least one key.
            Worst:
                - When key is None: O(n) this occurs when none of the slots in the top-level hash table contain any keys.
                - When key is not None: O(m) this occurs when the desired top-level key is not found in the table,
                                        or its associated sub-table is empty.
        """
        keys = []

        if key is None:
            for i in range(self.table_size):
                if self.array[i] is not None:
                    keys.append(self.array[i][0])
        else:
            position = self._linear_probe(key, None, False)
            sub_table = self.array[position][1]
            for index in range(sub_table.table_size):
                if sub_table.array[index] is not None:
                    keys.append(sub_table.array[index][0])

        return keys

    def values(self, key: K1 | None = None) -> list[V]:
        """
        Returns a list of values in the hash table.

        Params:
            key (K1 | None): If None, returns all values in the entire double key hash table.
                             If not None, returns all values in the sub-table of the given top-level key.

        Returns:
            list[V]: A list of values.

        Raises:
            None.

        Complexity:
            Best:
                - When key is None: O(n + m) this occurs when the first slot in the top-level hash table contains
                                    a non-empty sub-table, and this sub-table has at least one value.
                - When key is not None: O(m) this occurs when the desired top-level key is found in the table
                                        and its associated sub-table has at least one value.
            Worst:
                - When key is None: O(n + m) this occurs when none of the slots in the top-level hash table contain any values,
                                    or all associated sub-tables are empty.
                - When key is not None: O(m) this occurs when the desired top-level key is not found in the table,
                                        or its associated sub-table is empty.
        """
        values = []

        if key is None:
            for item in self.array:
                if item is not None:
                    sub_table = item[1]
                    values.extend(sub_table.values())
        else:
            position = self._linear_probe(key, None, False)
            sub_table = self.array[position][1]
            values.extend(sub_table.values())

        return values


    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks if the given key is in the Hash Table.

        Params:
            key (tuple[K1, K2]): The key pair to check for existence.

        Returns:
            bool: True if the key is found, False otherwise.

        Raises:
            None.

        Complexity:
            See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value associated with a certain key pair.

        Params:
            key (tuple[K1, K2]): The key pair to retrieve the value for.

        Returns:
            V: The value associated with the given key pair.

        Raises:
            KeyError: When the key pair doesn't exist.

        Complexity:
            See linear probe.
        """
        position1, position2 = self._linear_probe(key[0], key[1], False)
        return self.array[position1][1].array[position2][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set a (key, value) pair in the hash table.

        Params:
            key (tuple[K1, K2]): The key pair.
            data (V): The value to be associated with the key pair.

        Returns:
            None.

        Raises:
            None.

        Complexity:
            See linear probe.
        """
        key1, key2 = key
        position1, position2 = self._linear_probe(key1, key2, True)
        sub_table = self.array[position1][1]

        if sub_table.is_empty():
            self.count += 1

        sub_table[key2] = data

        # resize if necessary
        if len(self) > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair from the hash table.

        Params:
            key (tuple[K1, K2]): The key pair to be deleted.

        Returns:
            None.

        Raises:
            KeyError: When the key pair doesn't exist.

        Complexity:
            Best:
                - O(1) this occurs when the key pair is found without probing.
            Worst:
                - O(N*hash(K) + N^2*comp(K)) this occurs when there's lots of probing involved.
                  Where N is the size of the table, hash(K) is the hash function complexity,
                  and comp(K) is the comparison complexity.
        """
        key1, key2 = key
        key1_position, key2_position = self._linear_probe(key1, key2, False)

        if self.array[key1_position] is None or self.array[key1_position][1].array[key2_position] is None:
            raise KeyError(key)

        sub_table = self.array[key1_position][1]
        sub_table.array[key2_position] = None

        if all(value is None for value in sub_table.array):
            self.array[key1_position] = None
            self.count -= 1

            position = (key1_position + 1) % self.table_size
            while self.array[position] is not None:
                key1, sub_table = self.array[position]
                self.array[position] = None

                new_position = self._linear_probe(key1, None, True)
                self.array[new_position] = (key1, sub_table)
                position = (position + 1) % self.table_size


    def _rehash(self) -> None:
        """
        Resize the hash table and reinsert all key-value pairs.

        Params:
            None.

        Raises:
            None.

        Returns:
            None.

        Complexity:
            Best:
                - O(N*hash(K)) this occurs when no probing is required.
            Worst:
                - O(N*hash(K) + N^2*comp(K)) this occurs when there's lots of probing involved.
                  Where N is the size of the hash table, hash(K) is the hash function complexity,
                  and comp(K) is the comparison complexity.
        """
        old_array = self.array
        self.size_index += 1
        new_size = self.TABLE_SIZES[self.size_index]
        new_array = ArrayR(new_size)
        self.count = 0
        self.array = new_array

        for item in old_array:
            if item is not None:
                key1, sub_table = item

                new_position = self._linear_probe(key1, None, True)
                self.array[new_position] = (key1, sub_table)

                self.count += 1


    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()