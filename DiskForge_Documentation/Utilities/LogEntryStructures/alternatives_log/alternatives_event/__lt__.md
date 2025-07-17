# \_\_lt\_\_()
Adding less then functionality for the struct
## Parameters:
    def __lt__(self, other):
- other: The other event object
## Workflow:
    return self.timestamp_unix < other.timestamp_unix