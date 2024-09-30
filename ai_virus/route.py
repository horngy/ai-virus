"""
This module contains the dataclass RouteSplit, RouteSeries and Route
"""

from __future__ import annotations
from dataclasses import dataclass
from computer import Computer
from typing import TYPE_CHECKING, Union
from branch_decision import *

__author__ = "Adrian Ong Zhe Yee, Teh Yee Hong"

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from virus import VirusType


@dataclass
class RouteSplit:
    """
    A split in the route.
       _____top______
      /              \
    -<                >-following-
      \____bottom____/
    """

    top: Route
    bottom: Route
    following: Route

    def remove_branch(self) -> RouteStore:
        """Removes the branch, should just leave the remaining following route.

        Returns: a dataclass Route's store

        Complexity: O(1)
        """
        return self.following.store

@dataclass
class RouteSeries:
    """
    A computer, followed by the rest of the route

    --computer--following--

    """

    computer: Computer
    following: Route

    def remove_computer(self) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Removing the computer at the beginning of this series.

        Complexity: O(1)
        """
        return self.following.store

    def add_computer_before(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer in series before the current one.

        Complexity: O(1)
        """
        return RouteSeries(computer, Route(self))

    def add_computer_after(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer after the current computer, but before the following route.

        Complexity: O(1)
        """
        return RouteSeries(self.computer, Route(RouteSeries(computer, self.following)))

    def add_empty_branch_before(self) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding an empty branch, where the current routestore is now the following path.

        Complexity: O(1)
        """
        return RouteSplit(Route(None), Route(None), Route(self))

    def add_empty_branch_after(self) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding an empty branch after the current computer, but before the following route.

        Complexity: O(1)
        """
        return RouteSeries(self.computer, Route(RouteSplit(Route(None), Route(None), self.following)))

RouteStore = Union[RouteSplit, RouteSeries, None]


@dataclass
class Route:

    store: RouteStore = None

    def add_computer_before(self, computer: Computer) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding a computer before everything currently in the route.

        Complexity: O(1)
        """
        return Route(RouteSeries(computer, self))

    def add_empty_branch_before(self) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding an empty branch before everything currently in the route.

        Complexity: O(1)
        """
        return Route(RouteSplit(Route(None), Route(None), self))

    def follow_path(self, virus_type: VirusType) -> None:
        """
        Follow a path and add computers according to a virus_type.
        How it works is by separating the whole route into two parts,
        then solve each parts by breaking them down into more parts

        param arg1: a virus type

        Complexity: Best case occur when route is None, loop will not even start, complexity is O(1)
                    Worst case occur when nested loop occurs and worst case for there_is_still_more occur, Complexity is O(x * y * z)
                    where x is the number of outer loop, y is the number of nested loop and z is there_is_still_more occur
        """
        def there_is_still_more(route, virus_type):
            """
            This function is used to add the computers in the choosen route,
            and check whether there is still more "front" route to go to,
            if there's none, None will be return in "front"

            param arg1: a route (the whole route before separation into smaller parts)
            param arg2: a virus type

            Returns: "front", a route to be broken down if there's still more
                     "route", the continuing route
                     "choice", choice taken by the virus

            Complexity: Depending on virus_type.select_branch(route.top, route.bottom)
                        Best case occur when virus type is either a TopVirus or BottomVirus, Complexity is O(1)
                        Worst case occur when virus type is FancyVirus and both route are a RouteSeries, Complexity is O(n)
            """
            front = None
            choice = None
            if isinstance(route, RouteSeries):
                virus_type.add_computer(route.computer)
                route = route.following.store
            elif isinstance(route, RouteSplit):
                choice = virus_type.select_branch(route.top, route.bottom)
                if choice == BranchDecision.TOP:
                    front = route.top.store
                elif choice == BranchDecision.BOTTOM:
                    front = route.bottom.store
                elif choice == BranchDecision.STOP:
                    return None, None, choice
                route = route.following.store
            return front, route, choice

        route = self.store
        while route is not None:
            front, route, choice = there_is_still_more(route, virus_type)
            if choice == BranchDecision.STOP:
                break
            while front is not None:
                front1, front, choice = there_is_still_more(front, virus_type)
                if choice == BranchDecision.STOP:
                    route = None
                while front1 is not None:
                    front2, front1, choice = there_is_still_more(front1, virus_type)
                    if choice == BranchDecision.STOP:
                        front = None
                    while front2 is not None:
                        front3, front2, choice = there_is_still_more(front2, virus_type)
                        if choice == BranchDecision.STOP:
                            front1 = None
                        while front3 is not None:
                            front4, front3, choice = there_is_still_more(front3, virus_type)
                            if choice == BranchDecision.STOP:
                                front2 = None

    def add_all_computers(self) -> list[Computer]:
        """Returns a list of all computers on the route."""
        lst = []

        def there_is_still_more(route):
            """
            Check whether there is still more parts inside it, if yes, recursion will occur

            param arg1: the route to be checked

            Complexity: Best case occur when it is only a RouteSeries, complexity is O(n)
                        Worst case occur when the route is separated into a lot of parts, complexity is O(n)
            """
            if isinstance(route, RouteSeries):
                lst.append(route.computer)
                there_is_still_more(route.following.store)
            elif isinstance(route, RouteSplit):
                there_is_still_more(route.top.store)
                there_is_still_more(route.bottom.store)
                there_is_still_more(route.following.store)

        there_is_still_more(self.store)
        return lst

if __name__ == "__main__":
    pass