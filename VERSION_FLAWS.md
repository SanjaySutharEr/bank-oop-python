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

---

## Evolution Summary

| Version | Focus | Maturity |
|------|------|---------|
| V1 | Basic OOP | Beginner |
| V2 | Validation & structure | Intermediate |
| V3 | Invariants & descriptors | Advanced |
| V4 | Domain modeling | Near-production |

---

## Requirements for V5

- Account-number-based APIs only
- Atomic transfers (commit / rollback)
- Immutable transaction records
- Service layer separation
- Optional persistence (JSON / DB)

---

**V4 represents a real domain model.  
V5 should behave like a banking core, not a script.**
