import pytest

from models import Customer, Food, Menu, Transaction


# --- Fixtures ---------------------------------------------------------------


@pytest.fixture
def burger() -> Food:
    return Food("Spicy Burger", 5.0, "Mains", 4.5)


@pytest.fixture
def soda() -> Food:
    return Food("Large Soda", 2.0, "Drinks", 4.0)


@pytest.fixture
def cake() -> Food:
    return Food("Choc Cake", 6.0, "Desserts", 4.9)


@pytest.fixture
def menu(burger, soda, cake) -> Menu:
    """A menu in a known insertion order: burger, soda, cake."""
    return Menu([burger, soda, cake])


# --- Category filtering: Menu.filterByCategory ------------------------------


def test_filter_returns_matching_item(menu, soda):
    assert menu.filterByCategory("Drinks") == [soda]


def test_filter_no_match_returns_empty(menu):
    assert menu.filterByCategory("Soups") == []


def test_filter_multiple_matches():
    fries = Food("Fries", 3.0, "Mains", 4.2)
    burger = Food("Spicy Burger", 5.0, "Mains", 4.5)
    menu = Menu([fries, burger])
    assert menu.filterByCategory("Mains") == [fries, burger]


def test_filter_is_case_sensitive(menu):
    # Documents current behavior: matching is exact/case-sensitive.
    assert menu.filterByCategory("drinks") == []


def test_filter_does_not_mutate_menu(menu, burger, soda, cake):
    menu.filterByCategory("Drinks")
    assert menu.getItems() == [burger, soda, cake]


# --- Sorting: Menu.sortByPopularity -----------------------------------------


def test_sort_descending_default(menu, burger, soda, cake):
    # Ratings: cake 4.9, burger 4.5, soda 4.0 -> most popular first.
    assert menu.sortByPopularity() == [cake, burger, soda]


def test_sort_ascending(menu, burger, soda, cake):
    assert menu.sortByPopularity(descending=False) == [soda, burger, cake]


def test_sort_is_non_mutating(menu, burger, soda, cake):
    menu.sortByPopularity()
    # The menu's own order is left unchanged.
    assert menu.getItems() == [burger, soda, cake]


def test_sort_empty_menu():
    assert Menu().sortByPopularity() == []


def test_sort_stable_on_ties():
    # Equal ratings keep their relative insertion order (sorted is stable).
    first = Food("First", 1.0, "Mains", 4.5)
    second = Food("Second", 2.0, "Mains", 4.5)
    menu = Menu([first, second])
    assert menu.sortByPopularity() == [first, second]
    assert menu.sortByPopularity(descending=False) == [first, second]


# --- Total calculation: Transaction.computeTotal ----------------------------


def test_total_sums_prices(burger, soda):
    t = Transaction([burger, soda])
    assert t.computeTotal() == pytest.approx(7.0)


def test_total_empty_transaction_is_zero():
    assert Transaction().computeTotal() == pytest.approx(0.0)


def test_total_single_item(cake):
    t = Transaction()
    t.addItem(cake)
    assert t.computeTotal() == pytest.approx(6.0)


def test_total_with_duplicates(burger):
    t = Transaction([burger, burger])
    assert t.computeTotal() == pytest.approx(10.0)
