"""ByteBites domain models.

Four classes implementing the finalized UML in bytebites_design.md:
Food, Menu, Transaction, Customer. Each class follows the diagram literally —
private (name-mangled) fields exposed through explicit getter methods.
"""

from __future__ import annotations

from typing import List


class Food:
    """A single sellable item, e.g. a "Spicy Burger" or "Large Soda"."""

    def __init__(self, name: str, price: float, category: str, popularity_rating: float):
        self.__name = name
        self.__price = price
        self.__category = category
        self.__popularity_rating = popularity_rating

    def getName(self) -> str:
        return self.__name

    def getPrice(self) -> float:
        return self.__price

    def getCategory(self) -> str:
        return self.__category

    def getPopularityRating(self) -> float:
        return self.__popularity_rating


class Menu:
    """The full catalog of items; supports filtering by category."""

    def __init__(self, items: List[Food] = None):
        self.__items: List[Food] = items if items is not None else []

    def addItem(self, item: Food) -> None:
        self.__items.append(item)

    def removeItem(self, item: Food) -> None:
        self.__items.remove(item)

    def getItems(self) -> List[Food]:
        return self.__items

    def filterByCategory(self, category: str) -> List[Food]:
        return [item for item in self.__items if item.getCategory() == category]


class Transaction:
    """Groups the items a user picked and computes the total cost."""

    def __init__(self, selected_items: List[Food] = None):
        self.__selected_items: List[Food] = selected_items if selected_items is not None else []

    def addItem(self, item: Food) -> None:
        self.__selected_items.append(item)

    def getSelectedItems(self) -> List[Food]:
        return self.__selected_items

    def computeTotal(self) -> float:
        return sum(item.getPrice() for item in self.__selected_items)


class Customer:
    """A customer, tracked by name and past purchase history."""

    def __init__(self, name: str, purchase_history: List[Transaction] = None):
        self.__name = name
        self.__purchase_history: List[Transaction] = (
            purchase_history if purchase_history is not None else []
        )

    def getName(self) -> str:
        return self.__name

    def getPurchaseHistory(self) -> List[Transaction]:
        return self.__purchase_history

    def addTransaction(self, t: Transaction) -> None:
        self.__purchase_history.append(t)

    def isVerified(self) -> bool:
        """A real user has at least one past transaction."""
        return len(self.__purchase_history) > 0
