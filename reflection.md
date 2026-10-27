# Reflection

The handout says the reflection questions are "provided in the lab" but does not list them, so these four are written around its learning outcomes and this program.

## 1. What are the purpose and scope of static code analysis, and what did each tool catch in this program?

Static analysis examines source code without running it, to find bugs, vulnerabilities and style problems early. Each tool covers a different slice. Pylint (code quality) reported 22 messages and gave the file 6.27/10: missing docstrings, `global` statements, a bare `except`, files opened without `with`, a mutable default argument and a camelCase function name. Bandit (security) reported 3 issues: unsafe `pickle.load` (B301, Medium), the pickle import (B403, Low) and `try/except/pass` (B110, Low). Flake8 (PEP 8 style) reported 12 issues: missing blank lines (E302, E305), long lines (E501) and a bare `except` (E722). The scope has limits. None of the tools flagged that `"teleported"` was accepted as a status, that unknown dishes silently cost 99, or that empty orders were created. I only found those by running the program and reading its output, so static analysis complements testing and does not replace it.

## 2. How did you interpret the reports and prioritise fixes by severity?

I started with Bandit because it ranks findings by severity and confidence. The Medium finding (B301, pickle deserialization, CWE-502) came first because it can lead to code execution. The two Low findings (B403, B110) were fixed in the same commit. I then used Pylint's message categories: warnings (W) and refactor (R) messages such as W0102, W0603, W0702, W0718 and R1732 point at real risks, while convention (C) messages such as docstrings and naming are about maintainability. Flake8 came last because every item is formatting and cannot change behaviour. After each commit I reran that tool and the program to confirm the issues were gone: Bandit 0 issues, Pylint 10.00/10, Flake8 0 issues.

## 3. Which common Python issues were in the code, and how did you resolve them?

- **Mutable default argument (W0102):** `order_history=[]` is created once and shared by every call. I changed the default to `None` and only append when a list is passed in.
- **Overly broad or silent exceptions (W0702, W0718, E722, B110):** the bare `except: pass` in `update_order_status` hid every failure, and `except Exception` in `read_menu_config` hid file and JSON errors. The first now raises `ValueError` or `KeyError`, which `main` catches and reports; the second catches only `OSError` and `json.JSONDecodeError`.
- **Insecure coding pattern (B301, B403):** `pickle.load` on a file can execute arbitrary code if the file is tampered with. I replaced pickle with JSON and converted order ids back to `int` on restore, because JSON keys are strings.
- **Resource handling and globals (R1732, W1514, W0603):** files are now opened with `with open(..., encoding="utf-8")`, and `orders` and `menu` are mutated in place so no `global` statement is needed.

## 4. How did static analysis contribute to the code's quality and maintainability, and how would you use it in future work?

The code went from 6.27 to 10.00 on Pylint, from 3 Bandit issues to 0, and from 12 Flake8 issues to 0. It now has docstrings on every function, snake_case names, specific exceptions, no global state and a `__main__` guard, so it is easier to read, reuse and test, and the unsafe pickle path is gone. In future work I would run Flake8 and Pylint in the editor while coding, run all three tools in a pre-commit hook, and run them again in CI on every pull request. Bandit would block a merge on Medium or High findings, and Pylint would have an agreed minimum score. I would still read the program's output and write tests, because the tools cannot judge whether the program's rules are correct.
