'''
Problem: Die Logfiles haben teilweise nur das Datum ohne Jahr drinnen
Wir hätten aber gerne auch das Jahr also muss ich rausfinden woher die des Jahr haben
Beispiel ohne Jahreskontext:
Nov 23 15:24:46 niclas-VirtualBox kernel: [    2.672643] loop8: detected capacity change from 0 to 109072
Beispiel mit Epochensekunden (siehe audit(<EPOCHSECONDS>)):
Nov 23 15:24:46 niclas-VirtualBox kernel: [    4.070617] audit: type=1400 audit(1700749473.067:3): apparmor="STATUS" operation="profile_load" profile="unconfined" name="nvidia_modprobe" pid=350 comm="apparmor_parser"
Beispiel mit Datum im Infotext:
Nov 23 15:25:48 niclas-VirtualBox anacron[537]: Anacron 2.3 started on 2023-11-23
Nov 23 15:25:48 niclas-VirtualBox kernel: [    0.564831] rtc_cmos rtc_cmos: setting system clock to 2023-11-23T14:25:43 UTC (1700749543)

Unter der Annahme, dass alles chronologisch ist in dem Logfile, können wir dadurch bestimmen was die anderen Events für Jahre haben
Indem wir schauen welches näheste Event ein Jahr hat und wie beide Events zueinander stehen
Das ist dementsprechend wichtig, dass wir das Event wessen Timestamp wir verändern danach wieder an der richtige Stelle einsetzen
Wir könnten zwar einfach nur den Timestamp des Events ändern, aber das würde Spuren hinterlassen (wäre aber einfacher)
Im Plaso Source Code gibt es ein File plaso-main/plaso/lib/yearless_helper.py
Dort ist der Ansatz wie die des Jahr wiederherstellen wollen
Daran ws Orientieren
Können wir evt Plaso nutzen um für uns die Arbeit zu machen?

Erstmal Plan:
Soviel Temporale Daten aus diesen Events ziehen

Okay neuer Plan:
- Per icat die Syslog Datei holen
- Bereinigen von nicht printable Zeichen denn der shit macht zeug kaputt
- Auf die bereinigte Datei psteal werfen
- Matchen von psteal und syslog um im syslog Jahreszeitstempel zu haben
- Dann event nehmen und an der richtigen Stelle einfügen
- Neue Datei zurückschreiben
- Wahrscheinlich dann noch in den Metadaten die Länge anpassen

#TODO also irgendwie fehlt hier was vom Code!!!

Step 1: Get File per icat
'''
import re
from datetime import datetime

from Utility.SleuthKit.ExtractValuesFromIstat import istat_extract_inode
from Utility.Other import ParseTimestamps
from Utility.Parser import CSVParser
import Utility.Other.Terminal_Commands as commando
from Utility.Other.WriteTimeModLog import writeStderr

sample_text = """
Nov 23 15:24:46 niclas-VirtualBox anacron[492]: Anacron 2.3 started on 2023-11-23
Nov 23 15:24:46 niclas-VirtualBox kernel: [    0.221736] audit: type=2000 audit(1700749473.757:1): state=initialized audit_enabled=0 res=1
Nov 23 15:24:46 niclas-VirtualBox kernel: [    0.384147] NET: Registered PF_UNIX/PF_LOCAL protocol family
Nov 23 15:24:46 niclas-VirtualBox acpid: 8 rules loaded
Nov 23 15:24:58 niclas-VirtualBox gnome-shell[883]: GNOME Shell started at Thu Nov 23 2023 15:24:52 GMT+0100 (CET)
Nov 23 15:26:07 niclas-VirtualBox gnome-initial-setup[1282]: time=\"2023-11-23T15:26:07+01:00\" level=info msg=\"no DCD information: couldn't open /var/lib/ubuntu_dist_channel: open /var/lib/ubuntu_dist_channel: no such file or directory\"
"""

months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
          "Nov": 11, "Dec": 12}


def get_indexes_by_timestamp(data, target_timestamp, target_message):
    return [index for index, item in enumerate(data) if
            item.get('timestamp') == target_timestamp and item.get('message').replace(",", " ").replace(" ",
                                                                                                        "") == target_message.replace(
                " ", "")]


def remove_null_bytes(file,verbose=False):
    """
    The remove_null_bytes function is used to remove null bytes from a file.
        
    
    :param file: Open the file and read it
    :param verbose: Print out the number of zero bytes removed
    :return: 0 on success or - 1 on error
    """
    try:
        with open(file, 'rb') as infile:
            content = infile.read()

    except OSError as e:
        writeStderr(f"{type(e)}: {e}")
        print(f"{type(e)}: {e}")
        return -1
    len_cont = len(content)
    # Remove null bytes from the content
    cleaned_content = content.replace(b'\x00', b'')
    if not len_cont == len(cleaned_content):
        print(f"Remove Null Bytes found zero bytes. {len_cont-len(cleaned_content)} zero bytes were erased.\n")

    try:
        with open(file, 'wb') as outfile:
            outfile.write(cleaned_content)

    except OSError as e:
        writeStderr(f"{type(e)}: {e}")
        print(f"{type(e)}: {e}")
        return -1

    return 0


def year_generator_simple(parsedLogs, image_location, inode_number, partition_to_use, verbose=False):
    # TODO also add Unixtime
    inode_data = istat_extract_inode(imagepath=image_location, inode_number=inode_number,
                                     offset=str(partition_to_use.start), verbose=verbose)
    last_modified = inode_data.file_modified
    last_modified_year = int(last_modified[0:4])
    last_month = 0
    for i in range(len(parsedLogs)):
        if i == 0:
            parsedLogs[i]["year"] = str(last_modified_year)
            last_month = months[parsedLogs[i]["timestamp"][0:3]]
            parsedLogs[i]["unixtime"] = generate_epochtime(parsedLogs[i]["timestamp"], parsedLogs[i]["year"])
        else:
            this_month = months[parsedLogs[i]["timestamp"][0:3]]
            if this_month > last_month:
                last_modified_year -= 1
            last_month = this_month
            parsedLogs[i]["year"] = str(last_modified_year)
            parsedLogs[i]["unixtime"] = generate_epochtime(parsedLogs[i]["timestamp"], parsedLogs[i]["year"])

    '''
    Einfach das Jahr nehmen aus den Metadaten
    Und dann von oben nach Unten durchgehen und beim Wechsel eines Jahres (NumMonatNeu > NumMonatAlt) Jahr um eins reduzieren
    '''
    return parsedLogs


def year_generator_complex(parsedLogs):
    # TODO also add Unixtime
    commando.remove("./registrar.csv")

    commando.psteal("./UbuntuSyslog", "registrar.csv")
    commando.find_delete("plaso")

    csv_data = CSVParser.parse_csv("../../../TestStuff/registrar.csv")

    for i in range(len(csv_data)):
        timestamp = ParseTimestamps.log2timeline_2log(csv_data[i]["datetime"])
        message = csv_data[i]["message"]
        closing_bracket = message.find(']')
        message = message[closing_bracket + 1:].strip()
        temp = get_indexes_by_timestamp(parsedLogs, timestamp[0], message)
        for j in range(len(temp)):
            parsedLogs[temp[j]]["year"] = timestamp[1]
            parsedLogs[temp[j]]["unixtime"] = generate_epochtime(parsedLogs[temp[j]]["timestamp"],
                                                                 parsedLogs[temp[j]]["year"])
    return parsedLogs


def generate_epochtime(logstring, year):
    '''
    Generates the Epochtime in Seconds
    Used for BinarySearchLater
    '''
    month = months[logstring[0:3]]

    date_string = year + "-" + str(month) + "-" + logstring[4:]
    # Define the format of your date and time string
    date_format = "%Y-%m-%d %H:%M:%S"  # Adjust this format based on your input

    try:
        # Parse the string to a datetime object
        dt_object = datetime.strptime(date_string, date_format)

        # Get the Unix timestamp in seconds
        unix_timestamp = int(dt_object.timestamp())

        return unix_timestamp

    except ValueError:
        writeStderr("Invalid date format")
        print("Error: Invalid date format")
        return -1


def syslogParser(logname):
    # TODO we funktioniert dass noch mal lol
    '''
    DAS IST DIE WICHTIGE METHODE!!!
    Das Syslog Pattern Parsed einen Syslog Timestamp und spaltet ein Event in folgende Teile
    timestamp: Der Zeitstempel in Format <MMM> <DD> <hh>:<mm>:<ss>
    hostname: Der hostname unter dem dieser Eintrag angelegt wurde
    process: Der Prozess welcher dieses Event angelegt hat
    pid: Welche Process ID der Prozess hatte
    message: Die Message des Event. Hier können weitere temporale Daten liegen
    :return: parsed logs on success and -1 on error
    '''

    '''
    The Patterns to identify syslog entries. We need two patterns, cause some process events look different
    '''
    pattern_syslog_event = re.compile(
        r'(?P<timestamp>\w{3} \d{1,2} \d{2}:\d{2}:\d{2}) (?P<hostname>\S+) (?P<process>[^\[\]]+)(?:\[(?P<pid>\d+)\])?: (?P<message>.+)')
    pattern_syslog_event2 = re.compile(
        r'(?P<timestamp>\w{3} \d{1,2} \d{2}:\d{2}:\d{2}) (?P<hostname>\S+) (?P<process>[^[\]:]+): (?P<message>.+)'
    )

    parsed_logs = []
    try:
        '''
        So here we have a funny little special case
        Sometimes when trying to open a syslogfile we get errors
        This happens, because some bytes are ISO-8859-1 encoded (LATIN1)
        https://de.wikipedia.org/wiki/ISO_8859-1
        '''
        file = open(logname, 'r', encoding="ISO-8859-1")
        lines = file.readlines()
        for line in lines:
            '''
            afaik only imuxsock makes problems
            '''
            # TODO further testing required
            if line.__contains__("[") and not line.__contains__(
                    "imuxsock"):  # TODO die Unterscheider hier besser machen
                matches = pattern_syslog_event.finditer(line)
                for match in matches:
                    log_dict = match.groupdict()
                    log_dict['timestamp'] = match.group(
                        'timestamp')
                    log_dict['year'] = None
                    log_dict['unixtime'] = None
                    parsed_logs.append(log_dict)
            elif line.__contains__("imuxsock") or not line.__contains__("["):
                matches = pattern_syslog_event2.finditer(line)
                for match in matches:
                    log_dict = match.groupdict()
                    log_dict['timestamp'] = match.group(
                        'timestamp')
                    log_dict['year'] = None
                    log_dict['unixtime'] = None
                    parsed_logs.append(log_dict)
            else:
                print("Error, line couldnt be parsed: {}".format(line))
            # TODO Errorlogging wenn kein Hit

    except OSError as e:
        writeStderr(f"{type(e)}: {e}")
        print(f"{type(e)}: {e}")
        return -1
    return parsed_logs
