# MySQL DDL Watcher

Detect changing MySQL DDL statement and notification changed information

You have to override your own notification method

---
```python
class MyWatcher(MySQLDDLWatcher):
     def _notification(self, diffs):
        # do stuff
```