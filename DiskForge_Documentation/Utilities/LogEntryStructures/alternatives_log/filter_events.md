# filter_events()
Function to filter events
## Parameters:
    def filter_events(events, timestamp, message):
- events: List of all events
- timestamp: Timestamp which should be filtered
- message: Message which should be filtered
- **return:** Tuple of (filtered_events and rest)
## Workflow:
1. Filter for either Timestamp, Message or both