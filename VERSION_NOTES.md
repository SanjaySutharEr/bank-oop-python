# Bank System – Version Notes

## V1 – Working Version

### Goal
- Build a functional bank system using Python OOP

### Known Flaws
- Bank stores account numbers mapped to names instead of account objects
- Transfer logic ignores overdraft capability of CurrentAccount
- Subclasses rely on name-mangling to access balance
- Business logic mixed with print statements
- Transactions stored as strings

### Lessons Learned
- Ownership matters more than access
- Private attributes complicate inheritance
- Rules belong inside the domain object

## Version 2 (V2)

**Main changes and fixes:**

1. **Encapsulation / OOP**
   - Changed Account.__balance to Account._balance to allow subclass access
   - Removed dependency on private name-mangling in subclasses

2. **Bank structure**
   - Bank now owns account objects instead of just mapping account numbers to names
   - Can now access balances, deposit, withdraw, and transfer via Bank

3. **Transfer improvements**
   - Respects overdraft limit for CurrentAccount
   - Checks available balance for SavingsAccount
   - Rejects negative transfer amounts
   - Validates that both accounts exist before transfer
   - Logs transactions for both sender and receiver

4. **Transaction logging**
   - Deposit, Withdraw, Transfer, and Interest now log all activity
   - Bank.show_account_summary now prints transaction history

5. **Defensive programming**
   - Deposit and Withdraw reject negative amounts
   - Transfers validate amounts and accounts

   ## V3 – Descriptor-Based & Robust Version

**Main changes and fixes:**  

1. **Balance Descriptor**
   - Introduced `Balance` descriptor to manage all account balances.
   - Centralizes balance logic and automatically enforces validation.
   - Prevents deletion of balance and ensures all reads/writes are checked.

2. **Domain-Specific Validation**
   - Each account type implements `_validate_balance()`:
     - `SavingsAccount`: balance must be ≥ 0.
     - `CurrentAccount`: balance ≥ -overdraft_limit.
   - Deposit and withdrawal operations automatically respect these rules.

3. **Exception-Based Error Handling**
   - Replaced print statements with exceptions (`ValueError`, `NotImplementedError`) for invalid operations.
   - Ensures programmatically detectable errors and safer automated processing.

4. **Atomic & Future-Proof Transfer Logic**
   - Transfer validates that the receiving account can accept the deposit before moving money.
   - Supports any future account types with custom deposit rules.
   - Ensures both accounts remain consistent in case of failure.

5. **Simplified Balance Access**
   - Removed `get_balance()` method; balance can now be accessed directly via `account.balance`.
   - Descriptor ensures all reads/writes are validated automatically.

6. **Transaction Logging**
   - All operations (Deposit, Withdraw, Transfer, Interest) are logged automatically.
   - Bank.show_account_summary prints complete transaction history for auditing.

7. **Developer Notes**
   - Adding a new account type only requires implementing `_validate_balance()`.
   - No changes required in Bank or transfer logic for new account types.
   - Balance management is now fully encapsulated within the descriptor.

**Improvements over V2:**  
- Eliminated manual balance checks in Bank.transfer.
- Replaced ad-hoc account-type logic with domain-driven validation.
- All errors are explicit exceptions instead of silent print warnings.
- Prepared system for extensibility and cleaner OOP design.
