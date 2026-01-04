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