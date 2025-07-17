import re

sample_text = """
Nov 23 15:24:46 niclas-VirtualBox anacron[492]: Anacron 2.3 started on 2023-11-23
Nov 23 15:24:46 niclas-VirtualBox kernel: [    0.221736] audit: type=2000 audit(1700749473.757:1): state=initialized audit_enabled=0 res=1
Nov 23 15:24:46 niclas-VirtualBox kernel: [    0.384147] NET: Registered PF_UNIX/PF_LOCAL protocol family
Nov 23 15:24:46 niclas-VirtualBox acpid: 8 rules loaded
Nov 23 15:24:58 niclas-VirtualBox gnome-shell[883]: GNOME Shell started at Thu Nov 23 2023 15:24:52 GMT+0100 (CET)
Nov 23 15:26:07 niclas-VirtualBox gnome-initial-setup[1282]: time=\"2023-11-23T15:26:07+01:00\" level=info msg=\"no DCD information: couldn't open /var/lib/ubuntu_dist_channel: open /var/lib/ubuntu_dist_channel: no such file or directory\"
"""


def compare_regex_patterns(string, regex_pattern1, regex_pattern2):
    match1 = re.fullmatch(regex_pattern1, string)
    match2 = re.fullmatch(regex_pattern2, string)

    if match1 and match2:
        print("Both Match: {}".format(string))
        # Both patterns match, choose the one with the longer match
        if len(match1.group()) >= len(match2.group()):
            print("Group 1: {} & Group 2: {}".format(len(match1.group()),len(match2.group())))
            return regex_pattern1
        else:
            return regex_pattern2
    elif match1:
        return regex_pattern1
    elif match2:
        return regex_pattern2
    else:
        # Neither pattern matches
        print("No match: {}".format(string))
        return None


# Example usage:
input_string = sample_text
regex_pattern1 = re.compile(
    r'(?P<timestamp>\w{3} \d{1,2} \d{2}:\d{2}:\d{2}) (?P<hostname>\S+) (?P<process>[^\[\]]+)(?:\[(?P<pid>\d+)\])?: (?P<message>.+)')  # Example regex pattern 1
regex_pattern2 = pattern_syslog_event2 = re.compile(
    r'(?P<timestamp>\w{3} \d{1,2} \d{2}:\d{2}:\d{2}) (?P<hostname>\S+) (?P<process>[^\[\]:]+): (?P<message>.+)'
)  # Example regex pattern 2

for line in input_string.splitlines():
    #print(line)
    best_pattern = compare_regex_patterns(line, regex_pattern1, regex_pattern2)
    if best_pattern:
        print(f"The best matching regex pattern is: {best_pattern}\n")
    else:
        print("No pattern matches the input string.\n")

'''
So im Moment bekommen wir keine Matches was aber bissl komisch ist
'''
