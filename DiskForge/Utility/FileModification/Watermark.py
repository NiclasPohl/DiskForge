import mmap
import time

from Utility.SleuthKit.ExtractValuesFromIstat import convert_istat_to_timestamp
from Utility.Conversions.TimeConverter import time_to_hex, unixtime_to_hex
import Utility.Other.Terminal_Commands as commando
from Utility.Other.WriteTimeModLog import changedMetadata
from datetime import datetime

def get_pagesize():
    """
    The function `get_pagesize` retrieves the page size configuration value and returns it as an
    integer.
    :return: The function `get_pagesize` is returning the page size value retrieved from the system
    configuration using the `commando.getconf("PAGE_SIZE")` command. The value is then converted to an
    integer before being returned.
    """
    result = commando.getconf("PAGE_SIZE")
    result = int(result.stdout)
    return result


def setWaterMark(partitionoffset, image_location):

    pagesize = get_pagesize()
    with open(image_location, "r+b") as f:

        # Aktuelles Datum und Uhrzeit abrufen
        jetzt = datetime.now()
        adress = partitionoffset + 4096 - len(f"DiskForge was here: {jetzt}")
        usable_offset = adress // pagesize * pagesize
        usable_index = adress % pagesize
        mm = mmap.mmap(f.fileno(), pagesize, offset=usable_offset)
        text = f"DiskForge was here: {jetzt}"
        mm[usable_index:usable_index + 4096- len(f"DiskForge was here: {jetzt}")] = text.encode('utf-8')
        mm.flush()
        mm.close()
        f.close()