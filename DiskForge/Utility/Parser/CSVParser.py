import csv
from Utility.Other.WriteTimeModLog import writeStderr


def parse_csv(file_path):
    """
    The parse_csv function takes a file path as an argument and returns the parsed data.

    :param file_path: Specify the path to the plaso file
    :return: A list of dictionaries
    """
    data = []

    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['datetime', 'timestamp_desc', 'source', 'source_long', 'message', 'parser', 'display_name',
                          'tag']

            csvreader = csv.DictReader(csvfile, fieldnames=fieldnames)
            firstRow = True
            for row in csvreader:
                '''
                Skip First Row cause it contains the column names
                '''
                if (firstRow):
                    firstRow = False
                    continue
                cleaned_row = row
                '''
                Fill the entry with data and append it
                '''
                entry = {
                    'datetime': cleaned_row['datetime'],
                    'timestamp_desc': cleaned_row['timestamp_desc'],
                    'source': cleaned_row['source'],
                    'source_long': cleaned_row['source_long'],
                    'message': cleaned_row['message'],
                    'parser': cleaned_row['parser'],
                    'display_name': cleaned_row['display_name'],
                    'tag': cleaned_row['tag']
                }
                data.append(entry)
    except OSError as e:
        writeStderr(f"{type(e)}: {e}")
        print(f"{type(e)}: {e}")
        return -1
    return data
