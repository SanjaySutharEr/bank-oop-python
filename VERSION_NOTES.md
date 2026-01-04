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
