# match_log2log2timeline()
The function maches two timestamps together
## Parameters:
    def match_log2log2timeline(log, log2timeline):
- log: Match the date and time of the log file to that of the timeline
- log2timeline: Find the date in the log file
- **return:** A boolean value
## Workflow:
1. Split timestamp into multiple parts
2. Bring the parts in the same order as `log`
3. Compare