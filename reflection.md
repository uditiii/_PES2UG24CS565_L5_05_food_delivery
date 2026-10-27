# Reflection

## 1. Why did Bandit flag `pickle.load` in `restore_orders`, and what did you change?

Bandit reported B301 (Medium) on `pickle.load(open(file, "rb"))` and B403 on the `import pickle` line. Unpickling can run arbitrary code, so anyone who can edit or replace `orders.pkl` could run commands on the machine that restores the backup. I replaced pickle with JSON (`json.dump` / `json.load`), which can only produce plain data. JSON object keys are always strings, so `restore_orders` now converts order ids back to `int`. Without that, `update_order_status(1, ...)` would fail after a restore because the key would be `"1"`.

## 2. What was wrong with `order_history=[]` and the `try ... except: pass` in `update_order_status`, and how did you fix each one?

`order_history=[]` is a mutable default argument (Pylint W0102). The list is created once when the function is defined and shared by every call that does not pass its own, so ids from unrelated calls pile up in the same list. I changed the default to `None` and only append when the caller passes a list. The bare `except: pass` (Bandit B110, Pylint W0702, Flake8 E722) hid every failure, so `update_order_status(42, "delivered")` and `update_order_status(b, "teleported")` looked like they worked. It now raises `ValueError` for a status not in `VALID_STATUSES` and `KeyError` for an unknown order id, and `main` catches those two and prints a clear message.

## 3. Which bugs in this program did none of the three tools report, and how did you find and fix them?

Running the original program showed output that looked wrong, and no tool flagged any of it. `"teleported"` was stored as a real status. The unknown dish "sushi" silently cost 99 (`menu.get(i, 99)`), so Ravi's order totalled 249. An order with no customer and no items was created with a total of 0. Ids were also not updated after `restore_orders`, so new orders could overwrite restored ones. I fixed these by validating the status, raising `ValueError` for dishes not on the menu, for an empty customer name and for an empty order, and by computing the next id as `max(orders) + 1`. Static analysis checks how code is written, not whether the rules of the program are right, so running the program and reading its output is still necessary.

## 4. How did the changes improve the code, and how would you keep these checks running in future work?

Pylint went from 6.27 to 10.00, Bandit from 3 issues to 0, and Flake8 from 12 issues to 0. The code also has no `global` statements, docstrings on every function, `print_queue` in snake_case, `with open(..., encoding="utf-8")` for every file, specific exceptions instead of `except Exception`, and a `__main__` guard so importing the module no longer runs it. To keep this up I would run Flake8 and Pylint in the editor, run all three tools in a pre-commit hook, and run them again in CI on every pull request. Bandit would block the merge on Medium or High findings, and Pylint would have an agreed minimum score.
