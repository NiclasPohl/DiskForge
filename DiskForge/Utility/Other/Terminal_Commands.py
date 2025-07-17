from subprocess import run, PIPE
from Utility.Other.WriteTimeModLog import writeStderr
import sys


def hexdump(src, trg):
    command = "hexdump -v -C {} > {}".format(src, trg)
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    if (writeStderr(result.stderr) == -1):
        print(f"Error in hexdump({src},{trg})! Aborted programm execution!")
        sys.exit()
    return result


def icat(offset, image, inode, target):
    command = "icat -o {} \"{}\" {} > {}".format(offset, image, inode, target)
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    if (writeStderr(result.stderr) == -1):
        print(f"Error in icat({offset},{image},{inode},{target})! Aborted programm execution!")
        sys.exit()
    return result


def remove(files):
    '''
    Command for removing files
    :param files: File or Files that should be deleted
    :return: result
    '''
    if not isinstance(files, str):
        files = ' '.join(files)
    command = "rm {}".format(files)
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    # writeStderr(result.stderr)
    return result


def psteal(src, trg):
    command = "psteal.py --source {} -o dynamic -w {}".format(src, trg)
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    writeStderr(result.stderr)
    return result


def find_delete(ending):
    command = "find . -type -iname \*.{} -delete".format(ending)
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    writeStderr(result.stderr)
    return result


def touch(file):
    command = "touch {}".format(file)
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    writeStderr(result.stderr)
    return result


def fls(offset, imagepath, outputfilelocation=None):
    if outputfilelocation == None:
        command = "fls -p -r -o {} \"{}\"".format(offset, imagepath)
    else:
        command = "fls -p -r -o {} \"{}\" > {}".format(offset, imagepath, outputfilelocation)
    print(command)
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    print("RUN FINISHED")
    if (writeStderr(result.stderr) == -1):
        print(f"Error in fls({offset},{imagepath},{outputfilelocation})! Aborted programm execution!")
        sys.exit()
    return result


def fsstat(offset, imagepath):
    command = "fsstat -o {} \"{}\"".format(offset, imagepath)
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    if (writeStderr(result.stderr) == -1):
        print(f"Error in fsstat({offset},{imagepath})! Aborted programm execution!")
        sys.exit()
    return result


def istat(offset, imagepath, inodenumber):
    command = "istat -o {} \"{}\" {}".format(offset, imagepath, inodenumber)
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    if (writeStderr(result.stderr) == -1):
        print(f"Error in istat({offset},{imagepath},{inodenumber})! Aborted programm execution!")
        sys.exit()
    return result


def mmls(imagepath):
    command = "mmls \"{}\"".format(imagepath)
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    if (writeStderr(result.stderr) == -1):
        print(f"Error in mmls({imagepath})! Aborted programm execution!")
        sys.exit()
    return result


def getconf(parameter):
    command = "getconf {}".format(parameter)
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    if (writeStderr(result.stderr) == -1):
        print(f"Error in getconf({parameter})! Aborted programm execution!")
        sys.exit()
    return result


def runLogfileCommand(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    writeStderr(result.stderr)
    return result


def copy(original_file, target_file):
    command = "cp {} {}".format(original_file, target_file)
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    if (writeStderr(result.stderr) == -1):
        print(f"Error in copy({original_file},{target_file})! Aborted programm execution!")
        return -1
    return result


def getFileEncoding(filename):
    command = "file -bi {}".format(filename)
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    if (writeStderr(result.stderr) == -1):
        print(f"Error in {command}! Aborted programm execution!")
        return -1
    result = result.stdout
    result = result.split()[1]
    result = result.split("=")[1]
    return result


def checkIfUTF8(filename):
    command = "iconv -f utf8 {} -t utf8 -o /dev/null".format(filename)
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    if not result.stderr == "":
        return "ISO-8859-1"
    return "UTF-8"


def compress(filename):
    command = "gzip {}".format(filename)
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    if (writeStderr(result.stderr) == -1):
        print(f"Error in gzip({filename})! Aborted programm execution!")
        return -1
    return result


def decompress(filename):
    command = "gzip -d {}".format(filename)
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    if (writeStderr(result.stderr) == -1):
        print(f"Error in gzip({filename})! Aborted programm execution!")
        return -1
    return result

def ifind(blocknumber,imagefile, offset):
    command = f"ifind -o {offset} -d {blocknumber} \"{imagefile}\""
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout
