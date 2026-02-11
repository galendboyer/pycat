# REVERSE THE CONCATENATOR (Large file to small files)
# Sheraz Choudhary (Last updated: 2023-09-18)

import os
import argparse

def extract_individual_files(inputfile):
    try:
        with open(inputfile, 'r') as input:
            print("-f, --inputfile argument, {}, does exist.".format(inputfile))
            current_file_content = []  # Store content of the current file block
            current_rel_path = None   # Store the fully qualified path from the comments
            is_inside_block = False    # Track if we are inside a file block

            # Loop through all lines in the input file
            for line in input:
                # If FullyQualifiedFile comment get path and clear contents of previous block
                if line.startswith('-- FullyQualifiedFile: '):
                    current_rel_path = line[len('-- FullyQualifiedFile: '):].strip()
                    current_file_content = []

                # If BEFIN OF FILE comment mark in block to true
                elif line.startswith('-- BEGIN OF FILE'):
                    is_inside_block = True

                # If END OF FILE comment mark in block to false and write contents to file at specified path
                elif line.startswith('-- END OF FILE'):
                    is_inside_block = False
                    if current_rel_path and current_file_content:
                        print(current_rel_path)  # Will output full path+file written (optional)

                        # If last line extra empty line then remove it
                        if current_file_content[-1]=='\n':
                            del current_file_content[-1]

                        # Save the content of the previous file block
                        save_individual_file(current_rel_path, current_file_content)

                # Append content lines to the current file block if in a block
                elif is_inside_block:
                    current_file_content.append(line)

        print(f'Individual files have been extracted to the relative paths from current directory in the input file.')
        
    except Exception as e:
        print(f'An error occurred: {e}')

def save_individual_file(rel_path, content):
    # Determine the file name from the full path
    file_name = os.path.basename(rel_path)

    # Save the individual file
    with open(rel_path, 'w') as output:
        output.writelines(content)


def main():
    # command line arguments to replace original prompt based implementation
    parser = argparse.ArgumentParser(description='Deconcatenate input file into output files.')
  
    parser.add_argument("-f", "--inputfile", help="Input file path (file to deconcatenate)")
   
    args = parser.parse_args()

    # Error checking to ensure that inputfile is appropriately specified
    if args.inputfile == None:
        print("Input file to deconcatenate -i, --inputfile must be used.")
        exit()

    if args.inputfile != None:
        if not os.path.exists(args.inputfile):
            print("-i, --inputfile argument, {}, does not exist!".format(args.inputfile))
            exit()
        elif not os.path.isfile(args.inputfile):
            print("-i, --inputfile argument, {}, is not a file".format(args.inputfile))
            exit()    

    # If basic checks pass, then call the function to deconcatenate files
    extract_individual_files(args.inputfile)

if __name__ == "__main__":
    main()
