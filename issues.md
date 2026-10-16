# Lab 5 — Static Code Analysis Issues

| Issue | Tool | Original line | Description | Resolution |
|---|---|---|---|---|
| Mutable default argument | Pylint | 9 | Shared list between function calls | Replaced dates=[] with dates=None |
| Bare exception | Bandit/Pylint | 21 | Exceptions were silently ignored | Replaced with explicit error handling |
| Unsafe eval | Bandit | 45 | Arbitrary code execution risk | Replaced eval with restricted AST arithmetic |
| Negative fine | Logic | 25 | Negative overdue days generated negative fines | Used max(0, days_overdue) |
| Missing docstrings | Pylint | Multiple | Functions lacked documentation | Added module and function docstrings |
| Unsafe file handling | Pylint | 34–43 | File resources were opened manually | Used context managers and UTF-8 |
| Invalid naming | Pylint | 27 | renewBook violated naming convention | Renamed to renew_book |
| Unused import | Flake8 | 2 | os module was unused | Removed import |
| Formatting | Flake8 | Multiple | Blank-line and line-length violations | Corrected formatting |
