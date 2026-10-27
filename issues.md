# Issues Found and Fixed — `delivery_system.py`

Before: Pylint 6.27/10, Bandit 3 issues (1 Medium, 2 Low), Flake8 12 issues.
After: Pylint 10.00/10, Bandit 0 issues, Flake8 0 issues.
Reports are in `reports/before/` and `reports/after/`.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Unsafe pickle deserialization (B301, B403) | Security (Medium) | 2, 49 | `pickle.load` on `orders.pkl` can execute arbitrary code if the file is tampered with. | Replaced pickle with JSON (`json.dump` / `json.load`). Order ids are converted back to `int` on restore because JSON keys are strings. |
| Try/except/pass (B110) and bare `except` (W0702, E722) | Security (Low) / Bug | 22-25 | `update_order_status` swallowed every error, so invalid ids and statuses failed silently. | Removed the try/except. It now raises `ValueError` for a bad status and `KeyError` for an unknown order id; `main` catches both and prints a message. |
| Invalid status accepted | Logic bug | 21-25 | `"teleported"` was stored as a real status because `VALID_STATUSES` was never checked. | Validate the status against `VALID_STATUSES` before updating. |
| Mutable default argument (W0102) | Bug | 11 | `order_history=[]` is created once and shared between all calls. | Default is now `None`; the list is only appended to when the caller passes one. |
| Unknown dish silently costs 99 | Logic bug | 15 | `menu.get(i, 99)` charged a made-up price for dishes not on the menu (e.g. "sushi"). | Raise `ValueError` for any item not on the menu. |
| Empty order / empty customer accepted | Logic bug | 58-60 | An order with no customer and no items was created with total 0. | `create_order` raises `ValueError` if the customer name or the items are missing. |
| Order ids reset after restore | Logic bug | 47-49 | After `restore_orders` the global `next_id` was not updated, so new orders could overwrite restored ones. | The next id is now computed as `max(orders) + 1` at creation time. |
| Overly broad `except Exception` (W0718) | Quality | 32 | Hid every possible error while reading the menu file. | Catch only `OSError` and `json.JSONDecodeError`, then fall back to the default menu. |
| Files opened without `with` (R1732) | Quality / Resource leak | 30, 43, 49 | File handles could stay open if an error occurred. | Use `with open(...)` for all file access. |
| Missing encoding (W1514) | Quality | 30 | `open()` used the platform default encoding. | Pass `encoding="utf-8"`. |
| `global` statements and `next_id` name (W0603, C0103) | Quality | 7, 12, 28, 48 | Mutable global state was rebound inside functions. | `orders` and `menu` are mutated in place; the id counter was removed. No `global` is needed. |
| Missing docstrings (C0114, C0116) | Quality | 1, 11, 21, 27, 35, 42, 47, 51, 56 | Module and all functions were undocumented. | Added a module docstring and a docstring on every function. |
| `printQueue` naming (C0103) | Style | 51 | Function name is not snake_case. | Renamed to `print_queue`. |
| `%` string formatting (C0209) | Style | 52 | Old-style formatting. | Use an f-string. |
| `main()` runs on import | Quality | 70 | Importing the module ran the program. | Wrapped in `if __name__ == "__main__":`. |
| Missing blank lines (E302, E305) | Style (Flake8) | 11, 21, 27, 35, 42, 47, 51, 56, 70 | PEP 8 needs two blank lines around top-level definitions. | Added them. |
| Lines over 79 characters (E501) | Style (Flake8) | 16, 54 | Long lines hurt readability. | Wrapped the dict, sum expression and list literals across lines. |
