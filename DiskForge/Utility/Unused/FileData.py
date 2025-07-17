from Utility.File_Operations.OpenFiles import openFile


def getLinesfromFile(inputfile, linenumbers,verbose):
    specified_lines = []

    file = openFile(inputfile, "r",verbose)
    lines = file.readlines()

    for i in range(len(linenumbers)):
        specified_lines.append(lines[int(linenumbers[i])])
    return specified_lines


def removeLinesfromFile(inputfile, linenumbers,verbose):
    file = openFile(inputfile, "r",verbose)
    lines = file.readlines()

    file = openFile(inputfile, "w",verbose)
    for number, line in enumerate(lines):
        if number not in linenumbers:
            file.write(line)


def insertLinesintoFile(inputfile, linenumbers, lines,verbose):
    print(lines)
    file = openFile(inputfile, "r",verbose)
    contents = file.readlines()
    file.close()

    for i in range(len(lines)):
        # print(type(linenumbers))
        if isinstance(linenumbers, int):
            contents.insert(linenumbers, lines[i])
        else:
            if (i >= len(linenumbers)):
                contents.insert(linenumbers[len(linenumbers) - 1], lines[i])
            else:
                contents.insert(linenumbers[i], lines[i])

    file = openFile(inputfile, "w",verbose)
    contents = "".join(contents)
    file.write(contents)
    file.close()
