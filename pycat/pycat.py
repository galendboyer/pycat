# CONCATENATE FILES (Small files to one large file)

import os
import argparse

turnOffConcatBool = False
            
def combine_files_in_list_to_output(filelist, outputfile, releaseName):
    try:
        with open(outputfile, 'w') as output:
                
            if filelist != None and os.path.isfile(filelist):
                with open(filelist, 'r') as text_file:
                    for line in text_file:
                        full_path = os.path.join(os.getcwd(), line.strip())
                        relative_path = os.path.relpath(os.path.join(os.getcwd(), line.strip()))
                        if os.path.isfile(relative_path):
                            with open(relative_path, 'r') as file:
                                if turnOffConcatBool == False:
                                    output.write('--################################################################################\n')
                                    output.write(f'-- FullyQualifiedFile: {relative_path}\n')
                                    output.write('-- BEGIN OF FILE\n')
                                output.write(file.read())
                                if turnOffConcatBool == False:
                                    output.write('\n-- END OF FILE\n\n\n\n')
                        elif relative_path != ".":
                            print("FILE, {} DOES NOT EXIST".format(relative_path))

    except Exception as e:
        print(f'An error occurred: {e}')
        
def main():
    global turnOffConcatBool
    global noEpilogue
    
    # command line arguments to replace original prompt based implementation
    parser = argparse.ArgumentParser(description='Combine files into an output file.')
    parser.add_argument("-f", "--filelist", help="Fully qualified file that has list of files to concatenate")
    parser.add_argument("-o", "--outputfile", help="Output file path")
    parser.add_argument("-D", "--turnoffconcat", action='store_true', dest='turnoffconcat', help="Turn Off Deconcat Helper Lines?")
    parser.add_argument("-E", "--noepilogue", action='store_true', dest='noepilogue', help="Don't postpend the epilogue.sql file found within the release folder")

    args = parser.parse_args()

    if args.turnoffconcat == True:
        turnOffConcatBool = True
    else:
        turnOffConcatBool = False
         
    if args.noepilogue == True:
        noEpilogue = True
    else:
        noEpilogue = False
    
    filelist=args.filelist
    outputFile=args.outputfile
    if outputFile == None:
        print("outputFile, {}, must be specified!".format(outputFile))
        exit()        

    if filelist != None:
        if not os.path.exists(filelist):
            print("filelist, {}, does not exist!".format(filelist))
            exit()
        elif not os.path.isfile(filelist):
            print("filelist, {}, is not a file".format(filelist))
            exit()
        else:
            combine_files_in_list_to_output(filelist, outputFile, "XXX")
            
if __name__ == "__main__":
    main()
