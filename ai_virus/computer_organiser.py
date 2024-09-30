"""
This module contain ComputerOrganiser class
"""

from __future__ import annotations

from computer import Computer

__author__ = "Adrian Ong Zhe Yee, Teh Yee Hong"

class ComputerOrganiser:

    def __init__(self) -> None:
        self.computers = []

    def cur_position(self, computer: Computer) -> int:  # binary search O(log(N))
        """
        This function is used to find the position of the computer

        param arg1: the computer to find

        Complexity: Best case occur when there's no computer in the list, no looping and raising KeyError, Complexity is O(1)
                    Worst case occur when binary search occur a lot of times, Complexity is O(log(N))
        """
        low = 0
        high = len(self.computers) - 1
        while high >= low:
            mid = (low + high) // 2
            if self.computers[mid].hacking_difficulty < computer.hacking_difficulty:
                low = mid + 1
            elif self.computers[mid].hacking_difficulty > computer.hacking_difficulty:
                high = mid - 1
            else:
                if self.computers[mid].risk_factor < computer.risk_factor:
                    low = mid + 1
                elif self.computers[mid].risk_factor > computer.risk_factor:
                    high = mid - 1
                else:
                    if self.computers[mid].name > computer.name:
                        high = mid - 1
                    elif self.computers[mid].name < computer.name:
                        low = mid + 1
                    else:
                        return mid
        raise KeyError

    def add_computers(self, computers: list[Computer]) -> None:  # O(Mlog(M) + N)
        """
        This function is used to add the computer into the list

        param arg1: the list of computer to be added

        Complexity: Best case occur when there are nothing in the list of computers, Complexity is O(N)
                    Worst case occur when there are a lot of computers in the list to be added, Complexity is O(Mlog(M) + N)
        """

        def custom_index(computer):
            """
            This function is used to find the index where the computer belongs to

            param arg1: the computer to be added

            Complexity: Best case occur when there's nothing inside the list, Complexity is O(1)
                        Worst case occur when binary search take place alot of times, Complexity is O(log(M))
            """
            def custom_boolean(computer1, computer2):
                """
                This function returns True or False based on their computer's specification

                param arg1: the first computer
                param arg2: the second computer

                Returns: boolean

                Complexity: O(1)
                """
                if computer1.hacking_difficulty == computer2.hacking_difficulty:
                    if computer1.risk_factor == computer2.risk_factor:
                        if computer1.name > computer2.name:
                            return False
                        elif computer1.name < computer2.name:
                            return True
                    elif computer1.risk_factor > computer2.risk_factor:
                        return False
                    elif computer1.risk_factor < computer2.risk_factor:
                        return True
                elif computer1.hacking_difficulty > computer2.hacking_difficulty:
                    return False
                elif computer1.hacking_difficulty < computer2.hacking_difficulty:
                    return True

            low = 0
            high = len(self.computers) - 1
            while high >= low:
                mid = (high + low) // 2
                if custom_boolean(computer, self.computers[mid]):
                    high = mid - 1
                else:
                    low = mid + 1

            if high < 0:
                return 0
            return low

        for c in computers:
            index = custom_index(c)
            self.computers.insert(index, c)


if __name__ == "__main__":
    pass