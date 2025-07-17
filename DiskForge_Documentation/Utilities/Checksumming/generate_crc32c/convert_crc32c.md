# convert_crc32c()
The function `convert_crc32c` takes a CRC32C value, inverts it, converts it to a bytearray, and then reverses the order of the bytes before returning the result.
## Parameters:
    def convert_crc32c(crc32c_val):
- crc32c_val: The result of the crc32c algorithm
- **return:** The function `convert_crc32c` returns a reversed bytearray that represents the converted CRC32C value.

## Workflow:
1. Calculate `0xFFFFFFFF - crc32c_val`
2. Remove `0x`
3. Convert to byte array
4. Reverse to get correct endianess