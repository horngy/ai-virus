"""
This module stores ComputerManager class
"""

from __future__ import annotations
from computer import Computer
from double_key_table import DoubleKeyTable

__author__ = "Adrian Ong Zhe Yee, Teh Yee Hong"

class ComputerManager:

    def __init__(self) -> None:
        self.all_computers = DoubleKeyTable()

    def add_computer(self, computer: Computer) -> None:
        """
        This function helps to store the computer into the DoubleKeyTable

        param arg1: the computer to be added

        Complexity: The complexity of DoubleKeyTable's linear probe
        """
        self.all_computers[str(computer.hacking_difficulty), computer.name] = computer

    def remove_computer(self, computer: Computer) -> None:
        """
        This function helps to delete the computer in the DoubleKeyTable

        param arg1: the computer to be deleted

        Complexity: The complexity of DoubleKeyTable's __delitem__
        """
        del self.all_computers[str(computer.hacking_difficulty), computer.name]

    def edit_computer(self, old: Computer, new: Computer) -> None:
        """
        This function helps to delete the old computer and add the new one

        param arg1: the computer to be deleted
        param arg2: the computer to be added

        Complexity: The complexity of DoubleKeyTable's linear probe + The complexity of DoubleKeyTable's __delitem__
        """
        self.all_computers[str(new.hacking_difficulty), new.name] = new.hacking_difficulty
        del self.all_computers[str(old.hacking_difficulty), old.name]

    def computers_with_difficulty(self, diff: int) -> list[Computer]:
        """
        This function returns a list of computer with the given hacking difficulty

        param arg1: the hacking difficulty in integer

        Complexity: Best case occur when there's nothing in iter_values, Complexity is O(n)
                    Worst case occur when iter_values is full, Complexity is O(n)
        """
        lst = []
        for c in self.all_computers.iter_values(str(diff)):
            lst.append(c)
        return lst

    def group_by_difficulty(self) -> list[list[Computer]]:
        """
        This function returns a list of list separating their hacking difficulty

        Complexity: Best case occur when all the lst_lst are empty, Complexity is O(n^2)
                    Worst case occur when all lst_lst are full, Complexity is O(n^2)
        """
        lst = []
        for x in range(0, 10):
            lst_lst = self.computers_with_difficulty(x)
            if len(lst_lst) != 0:
                lst.append(lst_lst)
        return lst

if __name__ == "__main__":
    pass
