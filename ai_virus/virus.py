"""
This module contains all type of virus
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from computer import Computer
from route import Route, RouteSeries, RouteSplit
from branch_decision import BranchDecision

__author__ = "Adrian Ong Zhe Yee, Teh Yee Hong"

class VirusType(ABC):

    def __init__(self) -> None:
        self.computers = []

    def add_computer(self, computer: Computer) -> None:
        self.computers.append(computer)

    @abstractmethod
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        raise NotImplementedError()


class TopVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """Always select the top branch

        param arg1: the first route
        param arg2: the second route

        Returns: a branch decision
        """
        return BranchDecision.TOP  # Complexity : O(1)


class BottomVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """Always select the bottom branch

        param arg1: the first route
        param arg2: the second route

        Returns: a branch decision
        """

        return BranchDecision.BOTTOM  # Complexity : O(1)


class LazyVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        Try looking into the first computer on each branch,
        take the path of the least difficulty.

        param arg1: the first route
        param arg2: the second route

        Returns: a branch decision

        Complexity: Best case occur when none of the route or one of the route is a RouteSeries,
                    Worst case occur when both are a RouteSeries
                    Both case O(1)
        """
        top_route = type(top_branch.store) == RouteSeries
        bot_route = type(bottom_branch.store) == RouteSeries

        if top_route and bot_route:
            top_comp = top_branch.store.computer
            bot_comp = bottom_branch.store.computer

            if top_comp.hacking_difficulty < bot_comp.hacking_difficulty:
                return BranchDecision.TOP
            elif top_comp.hacking_difficulty > bot_comp.hacking_difficulty:
                return BranchDecision.BOTTOM
            else:
                return BranchDecision.STOP
        # If one of them has a computer, don't take it.
        # If neither do, then take the top branch.
        if top_route:
            return BranchDecision.BOTTOM
        return BranchDecision.TOP


class RiskAverseVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        This virus is risk averse and likes to choose the path with the lowest risk factor.

        param arg1: the first route
        param arg2: the second route

        Returns: a branch decision

        Complexity: Best case occur when none of the route or one of the route is a RouteSeries,
                    Worst case occur when both are a RouteSeries
                    Both cases O(1)
        """
        top_route = type(top_branch.store) == RouteSeries
        bot_route = type(bottom_branch.store) == RouteSeries
        if top_route and bot_route:
            top_comp = top_branch.store.computer
            bot_comp = bottom_branch.store.computer
            if top_comp.risk_factor == 0 and bot_comp.risk_factor == 0:
                if top_comp.hacking_difficulty < bot_comp.hacking_difficulty:
                    return BranchDecision.TOP
                elif top_comp.hacking_difficulty > bot_comp.hacking_difficulty:
                    return BranchDecision.BOTTOM
            elif top_comp.risk_factor == 0:
                return BranchDecision.TOP
            elif bot_comp.risk_factor == 0:
                return BranchDecision.BOTTOM

            top_comp_hv = max(top_comp.hacking_difficulty, top_comp.hacked_value / 2)
            bot_comp_hv = max(bot_comp.hacking_difficulty, bot_comp.hacked_value / 2)
            if top_comp_hv == bot_comp_hv:
                return BranchDecision.STOP
            elif top_comp_hv > bot_comp_hv:
                return BranchDecision.TOP
            elif bot_comp_hv > top_comp_hv:
                return BranchDecision.BOTTOM

        elif top_route:
            return BranchDecision.BOTTOM
        elif bot_route:
            return BranchDecision.TOP
        else:
            return BranchDecision.TOP

class FancyVirus(VirusType):
    CALC_STR = "7 3 + 8 - 2 * 2 /"

    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        This virus has a fancy-pants and likes to overcomplicate its approach.

        param arg1: the first route
        param arg2: the second route

        Returns: a branch decision

        Complexity: Best case occur when none of the route or one of the route is a RouteSeries, Complexity is O(1)
                    Worst case occur when both are a RouteSeries, Complexity is O(n) as calculations are needed
        """
        def calculator(lst):
            """
            This function is used to calculate the value

            param arg1: a list of mathematical equations

            Returns: an integer of the answer of the equation

            Complexity: Best case occur when there are only three elements in the list, meaning only one calculation are needed,
                        Worst case occur when there are just a lot of elements in the list, need to make a lot of calculations,
                        Both best and worst case are O(n)
            """

            def operation(n1, n2, symbol):
                """
                THis function is for mathematical operations

                param arg1: first value
                param arg2: second value
                param arg3: mathematical operators

                Return: an integer of the answer of the equation

                Complexity: O(1)
                """
                output = 0
                if symbol == "+":
                    output = n1 + n2
                elif symbol == "-":
                    output = n1 - n2
                elif symbol == "*":
                    output = n1 * n2
                elif symbol == "/":
                    output = n1 / n2
                return output

            while len(lst) != 1:
                result = operation(int(lst[0]), int(lst[1]), lst[2])
                lst = lst[3:]
                lst.insert(0, result)
            return lst[0]

        top_route = type(top_branch.store) == RouteSeries
        bot_route = type(bottom_branch.store) == RouteSeries
        if top_route and bot_route:
            self.CALC_STR = self.CALC_STR.split()
            result = calculator(self.CALC_STR)
            top_comp = top_branch.store.computer
            bot_comp = bottom_branch.store.computer
            if top_comp.hacked_value < result:
                return BranchDecision.TOP
            elif bot_comp.hacked_value > result:
                return BranchDecision.BOTTOM
            else:
                return BranchDecision.STOP

        elif top_route:
            return BranchDecision.BOTTOM
        elif bot_route:
            return BranchDecision.TOP
        else:
            return BranchDecision.TOP

if __name__ == "__main__":
    pass