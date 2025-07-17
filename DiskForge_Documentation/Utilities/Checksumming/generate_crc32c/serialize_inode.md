# serialize_inode()
The function `serialize_inode` takes inode data, inode number, filesystem UUID, and generation as
    input, and returns a serialized inode.

## Parameters:
    def serialize_inode(inode_data, inode_number, filesystem_uuid, generation):
- inode_data: The `inode_data` parameter typically contains information about a file or
    directory, such as permissions, timestamps, size, and pointers to data blocks. It is the actual data
    associated with an inode in a filesystem
- inode_number: The `inode_number` parameter represents the unique identifier of an inode
    within a filesystem. It is typically an integer value that identifies a specific inode within the
    filesystem
- filesystem_uuid: A filesystem_uuid is a unique identifier assigned to a file system. It is
    used to distinguish one file system from another
- generation: Generation typically refers to the version number or timestamp associated with a
    particular piece of data. In the context of file systems, it is often used to track changes to a
    file or directory. It helps in ensuring data consistency and integrity
- **return:** The function `serialize_inode` returns the serialized inode data, which is a combination of
    the filesystem UUID, inode number, generation, and inode data.

## Workflow:
1. append `filesystem_uuid + inode_number.to_bytes(4, byteorder='little') + generation + inode_data`