# 🏦 Bank Account Management System (V1 - V6)

A comprehensive Python-based banking system that evolves from basic procedural-style logic to an advanced **Event-Sourced (Ledger-based)** architecture. This project tracks my personal journey in mastering Object-Oriented Programming (OOP) and financial data integrity.

---

## 🌟 Project Overview
This system manages different types of bank accounts (Savings, Current) and handles complex operations like atomic transfers, transaction history, and overdraft management.

### Key Features
- **Account Types:** Savings (with interest) and Current (with overdraft limits).
- **Transaction Ledger:** Immutable records of every deposit, withdrawal, and transfer.
- **Financial Accuracy:** Uses the `Decimal` library to prevent floating-point rounding errors.
- **Data Integrity:** Implements Python Descriptors, Enums, and Frozen Dataclasses.
- **Atomic Transfers:** Ensures money isn't lost during account-to-account moves.

---

## 📈 My Learning Evolution (V1 ➡️ V6)
Unlike a standard project, this repository contains **6 distinct versions**. Each version represents a major upgrade in my coding logic:

1.  **V1 - V2:** **The Basics.** Setting up Inheritance and fixing Encapsulation.
2.  **V3 - V4:** **Safety First.** Adding Descriptors for validation and moving from string logs to Transaction Objects.
3.  **V5:** **Strict Typing.** Implementing Enums and Dataclasses to prevent manual data entry errors.
4.  **V6:** **The Ledger Model.** The final transition to calculating balances from transaction history (Event Sourcing) and using `Decimal` for math.

> 💡 **Deep Dive:** For a full breakdown of the struggles and logic changes in each version, read my [**Flaws and Improvements Log**](./VERSION_FLAWS_AND_IMPROVEMENTS.md).

---

## 🛠️ Technical Toolkit
- **Language:** Python 3
- **Core Concepts:**
    - **Encapsulation:** Protecting account data from direct mutation.
    - **Polymorphism:** Unique behavior for Savings vs. Current withdrawals.
    - **Descriptors:** Custom `__get__` and `__set__` logic for balance gates.
    - **Ledger Logic:** Deriving state from a sequence of events.

---



## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher installed.

### How to Run
1. Clone this repository:
   ```bash
   git clone [https://github.com/SanjaySutharEr/Bank_account_management_system.git](https://github.com/SanjaySutharEr/Bank_account_management_system.git)
2. Navigate to the folder
   ```bash 
   cd Bank_account_management_system
3. Run the application 
   ```bash
   python "Bank_account_management_system"
---

## 📝 Usage Example (V6 Logic)
- Here is how you can use the system to manage accounts and perform secure transfers:
   ```bash
    from banksystem_management import Bank, AccountType

    # 1. Initialize the Bank
    mybank = Bank()

    # 2. Create accounts (Current and Savings)
    mybank.create_account(AccountType.CURRENTACCOUNT, "4674", "Krish", 2000)
    mybank.create_account(AccountType.SAVINGSACCOUNT, "2345", "John Mehra", 2000)

    # 3. Perform Transactions
    # Deposits and Transfers create immutable Transaction records in the ledger
    mybank.accounts["4674"].deposit(400)
    mybank.transfer("4674", "2345", 1550)

    # 4. View Results
    # 'current_balance()' sums all transactions to provide the most accurate total
    print(mybank.get_account("4674"))
    print(f"Balance: {mybank.get_account('4674').current_balance()}")

    # 5. Review History
    print(mybank.get_account("4674").last_n_transactions(4))

---

## 👤 Author
  - **Sanjay Suthar**
  - [GitHub Profile](https://github.com/SanjaySutharEr)
---
*Disclaimer: This project was built for educational purposes to demonstrate OOP principles and Python growth.*

  
