# Issues Found and Fixed — `delivery_system.py`

Before: Pylint 6.27/10, Bandit 3 issues (1 Medium, 2 Low), Flake8 12 issues.
After: Pylint 10.00/10, Bandit 0 issues, Flake8 0 issues.
Reports are in `reports/before/` and `reports/after/`. Line numbers refer to the original starter file.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Unsafe pickle deserialization (B301, B403) | Security (Medium) | 2, 49 | `pickle.load` on `orders.pkl` can run arbitrary code if the file is tampered with. | Replaced pickle with JSON. Order ids are converted back to `int` on restore because JSON keys are strings. |
| Silent error handling (B110, W0702, E722) | Security (Low) / Bug | 22-25 | `try/except: pass` in `update_order_status` hid every failure. | Removed it. The function now raises `ValueError` or `KeyError`, and `main` catches and reports them. |
| Mutable default argument (W0102) | Bug | 11 | `order_history=[]` is created once and shared between all calls. | Default is now `None`; append only when a list is passed. |
| Invalid status or order id accepted | Logic bug | 21-25 | `teleported` was stored as a status because `VALID_STATUSES` was never checked. | Validate the status and the order id before updating. |
| Bad orders accepted | Logic bug | 15, 58-60 | Unknown dishes silently cost 99 (`menu.get(i, 99)`), and an order with no customer and no items was created. | `create_order` raises `ValueError` for unknown dishes, a missing customer or empty items. |
| Ids not updated after restore | Logic bug | 47-49 | `next_id` was not updated after `restore_orders`, so new orders could overwrite restored ones. | Next id is computed as `max(orders) + 1`. |
| Broad `except Exception` (W0718) | Quality | 32 | Hid every error while reading the menu file. | Catch only `OSError` and `json.JSONDecodeError`. |
| File handling and globals (R1732, W1514, W0603, C0103) | Quality | 7, 12, 28, 30, 43, 48, 49 | Files opened without `with` or an encoding, and `global` statements. | Use `with open(..., encoding="utf-8")`; mutate `orders` and `menu` in place. |
| Docstrings, naming, structure (C0114, C0116, C0103, C0209) | Style | 1, 11-56 | No docstrings, `printQueue` not snake_case, `%` formatting, `main()` ran on import. | Added docstrings, renamed to `print_queue`, used an f-string, added a `__main__` guard. |
| PEP 8 formatting (E302, E305, E501) | Style (Flake8) | 11-70 | Missing blank lines and two lines over 79 characters. | Added blank lines and wrapped long lines. |
