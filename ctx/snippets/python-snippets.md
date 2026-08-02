# Python Helper Snippets

```python
import os, sys

def find_project_root():
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(10):
        if os.path.isfile(os.path.join(d, "index.md")):
            return d
        d = os.path.dirname(d)
    return None
```
