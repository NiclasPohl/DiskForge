# DiskForge
<img src="Images/DiskForgeLogo3.jpeg" width="500">

DiskForge is a framework built to manipulate unmounted ext4 disk images.
Currently it supports Timestomping for Inode Metadata, various logfiles and databases.
The structure of this documentation is oriented at the directory and file structure of the frame work

The framework is structured as follows:
1. The [**main driver**](MainCode.md) code: This code gets executed by the user to run the framework
2. [**Modules**](Modules/Modules.md): Here are the different modules stored at the moment we have:
   1. [**Timestomping**](./Modules/Timestomping/Timestomping.md)
      1. [**Metadata**](./Modules/Timestomping/Metadata/Metadata.md)
      2. [**Logfiles**](./Modules/Timestomping/Logfiles/Logfiles.md)
      3. [**Databases**](./Modules/Timestomping/Databases/Databases.md)
   2. Experimental
3. [**Utilities**](Utilities/Utlities.md): Utilities store various code mechanisms for the workflow of the framework
   1. [**Calculations**](./Utilities/Calculations/Calculations.md)
      1. [**OffSetCalculator.py**](./Utilities/Calculations/Offset_Calculator.md)
   2. [**Checksumming**](./Utilities/Checksumming/Checksumming.md)
      1. [**generate_crc32c.py**](./Utilities/Checksumming/generate_crc32c/generate_crc32c.md)
   3. [**Conversions**](./Utilities/Conversions/Conversions.md)
      1. [**Time2EpochMicro.py**](./Utilities/Conversions/Time2EpochMicro/Time2EpochMicro.md)
      2. [**TimeConverter.py**](./Utilities/Conversions/TimeConverter/TimeConverter.md)
      3. [**Timestamp_to_unixtime.py**](./Utilities/Conversions/Timestamp_to_unixtime/Timestamp_to_unixtime.md)
   4. [**Database Structures**](./Utilities/DatabaseStructures/DatabaseStructures.md)
      1. [**chrome_history.py**](./Utilities/DatabaseStructures/chrome_history/chrome_history.md)
      2. [**database.py**](./Utilities/DatabaseStructures/database/database.md)
      3. [**firefox_places.py**](./Utilities/DatabaseStructures/firefox_places/firefox_places.md)
   5. [**File Operations**](./Utilities/File_Operations/File_Operations.md)
      1. [**ExtractBytesFromHexFile.py**](./Utilities/File_Operations/ExtractBytesFromHexFile/ExtractedBytesFromHexFile.md)
      2. [**OpenFiles.py**](./Utilities/File_Operations/OpenFiles/OpenFiles.md)
   6. [**File Modification**](./Utilities/FileModification/FileModification.md)
      1. [**timestamp_update.py**](./Utilities/FileModification/timestamp_update/timestamp_update.md)
      2. [**WriteByteToImageFileData.py**](./Utilities/FileModification/WriteByteToImageFileData/WriteByteToImageFileData.md)
   7. [**Log Entry Structures**](./Utilities/LogEntryStructures/LogEntryStructures.md)
      1. [**alternatives_log.py**](./Utilities/LogEntryStructures/alternatives_log/alternatives_log.md)
      2. [**apt_history.py**](./Utilities/LogEntryStructures/apt_history/apt_history.md)
      3. [**dpkg_log.py**](./Utilities/LogEntryStructures/dpkg_log/dpkg_log.md)
      4. [**sys_log.py**](./Utilities/LogEntryStructures/sys_log/sys_log.md)
   8. [**Other**](./Utilities/Other/Other.md)
      1. [**CompareParser.py**](./Utilities/Other/CompareParser/CompareParser.md)
      2. [**fsstat_parser2_0.py**](./Utilities/Other/fsstat_parser2_0/fsstat_parser2_0.md)
      3. [**ParseTimestamps.py**](./Utilities/Other/ParseTimestamps/ParseTimestamp.md)
      4. [**Terminal_Commands.py**](./Utilities/Other/Terminal_Commands/Terminal_Commands.md)
      5. [**WriteTimeModLog.py**](./Utilities/Other/WriteTimeModLog/WriteTimeModLog.md)
   9.  [**Parser**](./Utilities/Parser/Parser.md)
       1.  [**CSVParser.py**](./Utilities/Parser/CSVParser/CSVParser.md)
       2.  [**SyslogParser.py**](./Utilities/Parser/SyslogParser/SyslogParser.md)
   10. [**SleuthKit**](./Utilities/SleuthKit/SleuthKit.md)
       1.  [**ExtractValuesFromFLS.py**](./Utilities/SleuthKit/ExtractValuesFromFLS/ExtractValuesFromFLS.md)
       2.  [**ExtractValuesFromFSSTAT.py**](./Utilities/SleuthKit/ExtractValuesFromFSSTAT/ExtractValuesFromFSSTAT.md)
       3.  [**ExtractValuesFromIstat.py**](./Utilities/SleuthKit/ExtractValuesFromIstat/ExtractValuesFromIstat.md)
       4.  [**ExtractValuesFromMMLS.py**](./Utilities/SleuthKit/ExtractValuesFromMMLS/ExtractValuesFromMMLS.md)

Sample Execution Commands:

    python3 ./DiskForge.py --func timestomp --target logfile --mode change --img <Image Path>  --file var/log/syslog --partnum 6 --mess SMBIOS --nts 2024-11-13 20:15:00 --log_type syslog
    python3 ./DiskForge.py --func timestomp --target logfile --mode shift --img <Image Path>  --file var/log/syslog --partnum 6 --mess SMBIOS --nts 2024-11-13 20:15:00 --log_type syslog
