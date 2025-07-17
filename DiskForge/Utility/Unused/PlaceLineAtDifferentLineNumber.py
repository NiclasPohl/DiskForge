from Utility.File_Operations.OpenFiles import openFile


def move_line(input_file, output_file, line_number, destination_line_number,verbose):
    # Read the contents of the file
    file = openFile(input_file, "r",verbose)
    lines = file.readlines()

    # Remove the specified line
    line_to_move = lines.pop(line_number - 1)

    # Insert the line at the desired position
    lines.insert(destination_line_number - 1, line_to_move)

    # Write the modified contents to the output file
    file = openFile(input_file, "w",verbose)
    file.writelines(lines)


# Example usage:
input_file_path = './input_file'
output_file_path = './output.txt'
line_to_move_number = 3  # Replace with the desired line number
destination_line_number = 6  # Replace with the desired destination line number

move_line(input_file_path, input_file_path, line_to_move_number, destination_line_number)
