# Main Code

The *[DiskForge.py](https://faui1-gitlab.cs.fau.de/lena.voigt/thesis-manipulating-disk-images-timestomping/-/blob/233dadf7a69b3a9bea3dbdcb85e657845e8acd79/DiskForge/DiskForge.py)* file is executed by the user to run the framework.
The Code uses the argparse library to parse the arguments supplied.

## Parameters:

### Mandatory:
The following parameters are mandatory for the execution of DiskForge. Without them nothing will get executed.
- **func**: The functionality ("timestomping","experimental")
- **target**: The target we want to manipulate ("metadata", "logfile", "database")
- **mode**: Set the execution mode ("change", "shift", "copy", "swap", "reset", "scramble", "nuke")

### Optional:
The following parameters are optional. If an optional parameter is not given and is needed during runtime, DiskForge will prompt the user to submit the needed parameter.
#### General Parameters:
- **verbosity**: Increase the verbosity of the programm
- **img**: Path to image file
- **file**: Path to file which you wish to modify
- **partnum**: Partition Number
- **shift_type**: Unit which should be shifted ("second", "minute", "hour", "day")
- **shift_time**: How much of given type should be shifted
- **update_length**:Updates the Length of the value saved in the inode
#### Metadata
- **count**: Counter for the Scramble Operator, specifies how often the program should scramble
#### Logfiles
- **log_type**: The logtype used("syslog", "apt", "dpkg", "alternatives")
- **complex**: Use complex year generation mechanism
- **ts**: Target Timestamp YYYY-MM-DD hh-mm-ss
- **mess**: Target message
#### Databases
- **db_name**: The database you want to modify ("chrome", "firefox", "chromium", "other")
- **prim_key**: The primary key of the database
- **comp_mode**: Comparison Mode for SQL Query. Use strict for = else LIKE is used
- **WHERE**: The Where Statements. Format <Column1> <Value1> <Column2> <Value2> etc.
- **url**: Target URL
#### Rest
- **nts**: New Timestamp YYYY-MM-DD hh-mm-ss
- **nval**: The new Value for DB. Format: <Column> <Value>
- **timestamp**: New Timestamp