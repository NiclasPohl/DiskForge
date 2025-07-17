import re
import Utility.Other.Terminal_Commands as command
from Utility.File_Operations.OpenFiles import openFile


def extract_arguments(line):
    match = re.search(r'Namespace\((.*?)\)', line)
    if match:
        args_str = match.group(1)
        try:
            args = eval('dict(' + args_str + ')')
            return args
        except (SyntaxError, ValueError):
            return None
    return None


def print_non_none_values(args):
    if args is not None:
        commandline = "python3 /home/niclas/PycharmProjects/thesis-manipulating-disc-images-timestomping/TestStuff/TimeMod.py "
        for name, value in args.items():
            if value is not None:
                if isinstance(value, list):
                    dings = f"--{name}"
                    for v in value:
                        dings = "{} {}".format(dings, v)
                    commandline += dings + " "
                else:
                    if not value == False:
                        print(value)
                        # print(f"--{name} {value}")
                        commandline += f"--{name} {value} "
        print(
            commandline)  # Nice wir haben unsere Commandline Befehle Ready zum ausführen nun nur noch den Befehl ausführen
        print(command.runLogfileCommand(commandline).stderr)


def find_matching_lines(logfile_path, verbose):
    file = openFile(logfile_path, "r", verbose=verbose)
    for line_number, line in enumerate(file, start=1):
        args = extract_arguments(line)
        print_non_none_values(args)

# Replace 'your_logfile.log' with the actual path to your logfile
# find_matching_lines('/home/niclas/PycharmProjects/thesis-manipulating-disc-images-timestomping/TestStuff/Timestomp_Logfile2')
