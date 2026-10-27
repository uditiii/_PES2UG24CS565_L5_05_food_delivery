# Reflection

## 1. Which issues were the easiest to fix, and which were the hardest?

Easiest: the Flake8 issues (blank lines, line length) and the Pylint naming and docstring warnings, because the tool says exactly what to change and the change cannot alter behaviour. Hardest: replacing pickle. JSON turns integer keys into strings, so `restore_orders` had to convert them back, and I also had to make sure new order ids did not collide with restored ones. Removing the `except: pass` was also harder than it looks, because once errors are no longer swallowed, `main` has to handle them properly.

## 2. Did the static analysis tools report any false positives?

Not really. A few warnings were low value for a small script (for example, missing docstrings), but they were all valid. Bandit's pickle import warning (B403) is partly redundant with B301, which is the real risk, but it was fixed by the same change. The tools also have blind spots: none of them flagged that `"teleported"` was accepted as a status, that unknown dishes cost 99, or that empty orders were allowed. I found those by running the program and reading the output.

## 3. How would you integrate static analysis into your development workflow?

Run Flake8 and Pylint in the editor while coding, run all three tools in a pre-commit hook, and run them again in CI on every pull request so a failing check blocks the merge. Bandit should be a hard gate for Medium and High findings. Pylint should have an agreed minimum score, with a short, reviewed list of disabled checks rather than blanket ignores.

## 4. What tangible improvements did you see in the code after the fixes?

Pylint went from 6.27 to 10.00, Bandit from 3 issues to 0, and Flake8 from 12 issues to 0. More importantly, the program is now safer (no pickle deserialization) and more correct: invalid statuses, unknown dishes, empty orders and unknown order ids are rejected with clear errors instead of being silently accepted. It is also easier to read and reuse, with docstrings, no globals, snake_case names and a `__main__` guard.
