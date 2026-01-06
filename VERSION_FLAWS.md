# Bank Account Management System – Version Analysis (V1 → V4)

This document analyzes the evolution of the Bank Account Management System across
**four versions (V1–V4)**.

For each version, it documents:
- ❌ Design / OOP / logic flaws
- ✅ Improvements compared to the previous version

The intent is to clearly track architectural maturity and identify what must be
solved in **V5**.

---

## V1 – Initial Functional Prototype

### ❌ Flaws in V1

1. **Bank stores incorrect data**
   - `Bank.accounts` stores `{acc_number: account.name}` instead of account objects.
   - Bank cannot manage accounts beyond existence checks.

2. **Broken encapsulation**
   - `transfer()` accepts account objects directly.
   - Bank does not control access to its own accounts.

3. **Unsafe balance access**
   - Balance is private (`__balance`) but `CurrentAccount` mutates it using name-mangling.
   - Violates encapsulation and is brittle.

4. **Weak validation**
   - Zero deposits allowed.
   - Errors handled via `print()` instead of exceptions.

5. **Incorrect transfer logic**
   - Overdraft rules ignored.
   - Uses only `get_balance()`.

6. **Primitive transaction logging**
   - Transactions are unstructured strings.
   - No timestamps or direction metadata.

7. **Business logic mixed with I/O**
   - Core methods print output directly.
   - Makes code non-testable and non-reusable.

---

### ✅ What V1 Achieved

- Basic OOP structure
- Inheritance via `SavingsAccount` and `CurrentAccount`
- Introduced transaction history concept

---

## V2 – Structural Cleanup & Validation

### ❌ Flaws in V2

1. **Bank still depends on external objects**
   - `transfer(acc1, acc2, amount)` still bypasses Bank ownership.

2. **Type checking via strings**
   - Uses `acc_type == "SavingsAccount"`.
   - Breaks polymorphism.

3. **Balance is only conventionally protected**
   - `_balance` can still be modified freely.

4. **Silent failures**
   - Invalid deposits fail without errors.
   - Withdrawals still print instead of raising.

5. **Split responsibility**
   - Bank manages transfer transactions.
   - Accounts manage deposit/withdraw transactions.

---

### ✅ Improvements Over V1

- Bank stores account objects, not names
- Transfer validates:
  - Amount
  - Account existence
  - Overdraft rules
- Improved transaction history clarity
- Reduced direct balance tampering

---

## V3 – Descriptor-Driven Invariants

### ❌ Flaws in V3

1. **Transfer relies on side effects**
   - No pre-validation before withdraw.
   - Depends on exceptions indirectly.

2. **Regressed Bank API**
   - `find_account()` accepts account objects, not account numbers.

3. **Transactions still unstructured**
   - Strings only.
   - No timestamps or domain meaning.

4. **Generic exception messages**
   - Errors lack context and specificity.

5. **Interest indistinguishable from deposits**
   - No semantic separation.

---

### ✅ Improvements Over V2

- Balance enforced via descriptor
- Centralized invariant validation
- Proper polymorphism for overdraft rules
- Exceptions replace print-based errors
- Strong encapsulation of balance logic

---

## V4 – Domain-Driven Design

### ❌ Flaws in V4

1. **Transfer API still object-based**
   - Should accept account numbers only.

2. **No atomicity**
   - Withdraw may succeed while deposit fails.

3. **No rollback mechanism**
   - Partial state corruption possible.

4. **Mutable Transaction objects**
   - No immutability guarantees.

5. **In-memory only**
   - No persistence or serialization layer.

---

### ✅ Improvements Over V3

- Introduced `Transaction` domain object
- Timestamped, structured transaction logs
- Clean separation of responsibilities:
  - Bank → orchestration
  - Account → invariants
- Custom error messages per account type
- No print statements in core logic
- Descriptor-based balance enforcement retained

# Improvements in V5 Compared to V4

This document summarizes all concrete improvements introduced in **V5** of the Bank Management System compared to **V4**, based on identified flaws, design discussions, and fixes applied during iteration.

---

## 1. Transaction System Improvements

### 1.1 Enforced Transaction Immutability
- V4 allowed potential mutation of `Transaction` attributes after creation.
- V5 overrides `__setattr__` to prevent modification of already-set attributes.
- Uses `super().__setattr__` correctly to bypass custom logic during initialization.

**Impact:**  
Transactions are now true immutable event records.

---

### 1.2 Stronger Transaction Validation
- V4 had incomplete or loose validation of transaction metadata.
- V5 enforces:
  - Correct `TransactionType` via Enum
  - Positive numeric amounts
  - Mandatory `source_account` for `TRANSFER_IN`
  - Mandatory `target_account` for `TRANSFER_OUT`
  - No source/target for DEPOSIT, WITHDRAW, INTEREST

**Impact:**  
Invalid transaction states are now impossible to construct.

---

## 2. Balance Handling & Invariant Enforcement

### 2.1 Descriptor-Based Balance Enforcement
- V4 balance rules were partially enforced via procedural logic.
- V5 uses a `Balance` descriptor to:
  - Prevent negative opening balances
  - Enforce numeric-only balances
  - Block deletion of balance
  - Delegate validation to account-specific rules

**Impact:**  
Balance invariants are centralized, reusable, and impossible to bypass.

---

### 2.2 Polymorphic Balance Validation
- V4 had weaker or duplicated balance rules.
- V5 enforces balance constraints via `_validate_balance()`:
  - `SavingsAccount`: balance ≥ 0
  - `CurrentAccount`: balance ≥ -overdraft_limit

**Impact:**  
Account-specific financial rules are cleanly extensible without conditionals.

---

## 3. Transfer Logic Improvements

### 3.1 Clear Separation of TRANSFER_IN vs TRANSFER_OUT
- V4 mixed transfer logic and semantics.
- V5 explicitly records:
  - `TRANSFER_OUT` for sender
  - `TRANSFER_IN` for receiver

**Impact:**  
Transaction history is now semantically correct and auditable.

---

### 3.2 Safe Failure Ordering Under Stated Assumptions
- V4 had ambiguity around partial transfer failure.
- V5 ensures:
  - Debit (`transfer_to`) happens first
  - Credit (`transfer_from`) only executes if debit succeeds
- Assumes deposits cannot fail (explicit design decision).

**Impact:**  
No partial state corruption under current model assumptions.

---

## 4. Error Handling & Messaging

### 4.1 Account-Specific Error Messages
- V4 hardcoded or leaked generic errors.
- V5 allows account-level customization:
  - `withdraw_error_msg` overridden in `CurrentAccount`

**Impact:**  
Cleaner API surface and clearer user-facing errors.

---

## 5. Account & Bank Design Improvements

### 5.1 Clear Responsibility Boundaries
- V4 had logic bleed between Bank and Account responsibilities.
- V5 clarifies:
  - `Bank` → orchestration & lookup
  - `Account` → state changes & rules
  - `Transaction` → immutable event record

**Impact:**  
System follows proper object-oriented responsibility segregation.

---

### 5.2 Safer Account Creation
- V4 allowed looser initialization paths.
- V5 enforces:
  - Unique account numbers
  - Valid opening balances
  - Descriptor-based initialization safety

**Impact:**  
Accounts cannot enter invalid initial states.

---

## 6. Transaction History Improvements

### 6.1 Correct Last-N Transaction Retrieval
- V4 had ordering / return bugs in transaction history.
- V5 correctly:
  - Extracts last N transactions
  - Preserves chronological order

**Impact:**  
Transaction summaries now behave correctly.

---

## 7. Code Quality & Design Maturity

### 7.1 Removal of Redundant Code Paths
- V4 repeated logic with minor variations.
- V5 consolidates logic via:
  - Centralized `_record_transaction`
  - Descriptor-driven balance enforcement

**Impact:**  
Less duplication, higher maintainability.

---

### 7.2 Explicit Design Assumptions
- V4 had implicit assumptions.
- V5 explicitly documents and codes against:
  - No upper deposit limit
  - Deposit operations never failing
  - Transfer atomicity under current constraints

**Impact:**  
The system is internally consistent and defensible by design.


