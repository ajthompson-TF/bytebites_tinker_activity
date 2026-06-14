# ByteBites — UML Class Diagram

```mermaid
classDiagram
    class Customer {
        -String name
        -List~Transaction~ purchaseHistory
        +getName() String
        +getPurchaseHistory() List~Transaction~
        +addTransaction(Transaction t) void
        +isVerified() boolean
    }

    class Food {
        -String name
        -double price
        -String category
        -double popularityRating
        +getName() String
        +getPrice() double
        +getCategory() String
        +getPopularityRating() double
    }

    class Menu {
        -List~Food~ items
        +addItem(Food item) void
        +removeItem(Food item) void
        +getItems() List~Food~
        +filterByCategory(String category) List~Food~
    }

    class Transaction {
        -List~Food~ selectedItems
        +addItem(Food item) void
        +getSelectedItems() List~Food~
        +computeTotal() double
    }

    Customer "1" --> "*" Transaction : purchase history
    Menu "1" o-- "*" Food : catalogs
    Transaction "1" o-- "*" Food : selects
```

## How the spec maps to the design

| Class | Responsibility (from request) | Key members |
|-------|------------------------------|-------------|
| **Customer** | Track name + past purchases; verify a real user | `name`, `purchaseHistory: List<Transaction>`, `isVerified()` |
| **Food** | A single sellable item | `name`, `price`, `category`, `popularityRating` |
| **Menu** | Full collection of items; filter by category | `items: List<Food>`, `filterByCategory()` |
| **Transaction** | Group picked items; compute total | `selectedItems: List<Food>`, `computeTotal()` |

## Relationship rationale

- **Customer → Transaction** (1-to-many): purchase history is a list of past transactions, which also backs `isVerified()`.
- **Menu ◇— Food** (aggregation): the menu *holds* the full catalog of items but doesn't own their lifecycle.
- **Transaction ◇— Food** (aggregation, 1-to-many): a transaction holds a list of selected items (shared references owned by the `Menu`); `computeTotal()` sums their `price`.

## Notes

- The bidirectional `Transaction → Customer` back-reference from the earlier draft was removed. The spec only requires a customer to track its past transactions, so the back-pointer added a circular dependency without a clear need.
- If a transaction later needs to know which customer made it (e.g., for receipts or fraud checks), re-introduce a single bidirectional `Customer "1" -- "*" Transaction` association rather than two separate arrows.
