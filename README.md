# MySQL DDL Watcher

Detect changing MySQL DDL statement and notification changed information

You can make your own notification handler

---

```python
class MyHandler(object):
     def notification(self, diffs):
        # do stuff

watcher = MySQLDDLWatcher(...)        
handler = MyHandler()
watcher.add_notification_handler(handler)
watcher.watch()
```