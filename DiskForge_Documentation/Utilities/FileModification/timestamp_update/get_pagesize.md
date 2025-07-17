# get_pagesize()
The function `get_pagesize` retrieves the page size configuration value and returns it as an
    integer.
## Parameters:
    def get_pagesize():
- **return:** The function `get_pagesize` is returning the page size value retrieved from the system
    configuration using the `commando.getconf("PAGE_SIZE")` command. The value is then converted to an
    integer before being returned.

## Workflow:
1. Run command.getconf()
2. Convert to int