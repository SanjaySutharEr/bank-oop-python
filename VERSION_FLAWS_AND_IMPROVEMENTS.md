# My Journey: Bank Account Management System
**Reflections on my first Python OOP Project**

This document tracks my evolution from writing basic scripts to understanding complex Object-Oriented Programming (OOP) principles. Each version represents a "lightbulb moment" where I realized a flaw in my thinking and fixed it.

---

## 📈 The Evolution Summary

| Version | Focus | Key Learning |
| :--- | :--- | :--- |
| **V1** | Initial Setup | Basic Class & Inheritance structure. |
| **V2** | Encapsulation | Moving from `__private` to `_protected` for better subclassing. |
| **V3** | Logic Safety | Implementing **Descriptors** to automate balance validation. |
| **V4** | Data Structure | Switching from string-based logs to **Transaction Objects**. |
| **V5** | Constraints | Using **Enums** and **Dataclasses** to prevent typos and errors. |
| **V6** | Architecture | **Event Sourcing**: Calculating balance from a history of transactions. |

---

## 🚀 Version 1: The "Make it Work" Phase
**What I did:** Created basic classes for `Bank` and `Account` with simple inheritance for `Savings` and `Current` accounts.
- **The Struggle:** I was just trying to get the logic of depositing and withdrawing to work.
- **The Flaw:** Subclasses were "reaching inside" the parent class using name-mangling (like `_Account__balance`). It was messy.
- **Realization:** If I change the parent class, all my subclasses break. This isn't true encapsulation.

## 🛠 Version 2: Cleaning up the OOP
**What I did:** Switched from private (`__`) to protected (`_`) attributes. Improved the `Bank` class to own the actual objects, not just names.
- **The Struggle:** I realized my `transfer` method was "dumb"—it assumed the money always existed and the accounts were always valid.
- **The Flaw:** I was using `print()` statements to warn users about errors. If this were a real app, a print statement wouldn't stop a bad transaction from happening.
- **Improvement:** Added basic validation to check if accounts exist before transferring.

## 🛡 Version 3: Descriptors & Validation
**What I did:** Introduced **Python Descriptors** (`Balance` class) to manage how balances are set.
- **The Struggle:** I was repeating the same "is the balance positive?" check in ten different places.
- **The Flaw:** My `Bank` class was doing too much "babysitting." It was checking the overdraft limits of the accounts instead of the accounts checking themselves.
- **Improvement:** Centralized logic into `_validate_balance`. Now, the `Account` is responsible for its own rules.

## 📜 Version 4: Real-World Transactions
**What I did:** Created a dedicated `Transaction` class and started using the `datetime` module.
- **The Struggle:** Before this, "Transaction History" was just a list of strings. I couldn't actually *do* anything with that data.
- **The Flaw:** Strings are hard to search or filter. I needed objects.
- **Improvement:** Every action now creates a `Transaction` object with a timestamp, type, and amount.

## 🏗 Version 5: Enums & Composition
**What I did:** Used `Enum` for transaction types and moved to a **Composition** model where the Bank creates the accounts.
- **The Struggle:** I realized a user shouldn't be able to just "create" a bank account in thin air and then try to use it. It must be created *through* the bank.
- **The Flaw:** Using strings like "DEPOSIT" is dangerous—a single typo like "DEPST" would break the whole system.
- **Improvement:** Used `Enum` to make type-checking strict. Used `@dataclass` for transactions to make them cleaner.

## 💎 Version 6: The "Pro" Architecture (Final)
**What I did:** Switched to **Decimal** for money, made transactions **Immutable**, and moved to a **Ledger-based Balance**.
- **The Struggle:** Floating-point math (0.1 + 0.2 != 0.3) is dangerous for banks. Also, I realized that storing a `self.balance` variable is risky because it can be accidentally changed.
- **The Flaw:** If I just change the `balance` number, I lose the "truth" of why it changed.
- **The Big Improvement (Event Sourcing):** - I stopped storing the balance as a simple number. 
    - Instead, `current_balance()` now calculates the total by looking at every transaction in the bank's history. 
    - This is how real banks work! It's atomic and much harder to fake or break.
- **Correctness:** Used `Decimal` to ensure every penny is accounted for correctly.

---

## 🎓 What I Learned
1. **Encapsulation:** Keep your data safe. Don't let other classes touch your private variables.
2. **Atomic Operations:** A transfer is two things (withdraw + deposit). If one fails, both must fail.
3. **Data Integrity:** Using `frozen=True` on dataclasses ensures that once a transaction is recorded, it can never be changed.
4. **Logic Placement:** Put the rules where the data is. The `Account` knows its limits; the `Bank` just manages the accounts.

**This was my first Python project, and looking back from V6 to V1, I can see how much my logic has matured!**