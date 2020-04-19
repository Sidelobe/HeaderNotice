# -*- coding: utf-8 -*-
#
# This script inserts custom file headers in to every source file in a directory
# If there's an existing file header, it is removed, i.e. replaced
# © Lorenz Bucher, 2020. All rights reserved
# https://github.com/Sidelobe/HeaderNotice

from glob import glob
import sys
import os
import re

custom_header = r"""
//     __  ___       ___             _         __ 
//    /  |/  /_ __  / _ \_______    (_)__ ____/ /_
//   / /|_/ / // / / ___/ __/ _ \  / / -_) __/ __/
//  /_/  /_/\_, / /_/  /_/  \___/_/ /\__/\__/\__/ 
//         /___/               |___/              
//
//  © 2020 - all rights reserved
"""

def strip_lines_and_add_header(file, num_lines, header):
    lines = None
    with open(file, "r") as input:
        lines = input.readlines()
    with open(file, "w") as output:
        output.writelines(header)
        output.writelines("\n")
        output.writelines(lines[num_lines:])

def main():
    ##########
    header = custom_header
    header = header.strip("\n\r")  # remove first newline
    ##########

    path = sys.argv[1]
    if os.path.exists(sys.argv[1]):
        path = os.path.abspath(sys.argv[1])

    file_list = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith(('.hpp', '.cpp', '.h', '.c')):
                file_list.append(os.path.join(root, filename))

    # Matches C++ Style // (multiline) comments, including leading whitespace
    pattern_cpp = re.compile(r'(\s*\/\/.*)')
    # Matches C Style /* */ and doxygen /** */ (multiline) comments
    pattern_c = re.compile(r'(\s?\/\*(?:[^*]|[\r\n]|(?:\*+(?:[^*\/]|[\r\n])))*\*+\/)|(\s?\/\/.*)')

    for file_name in file_list:
        print "\n========================\nScanning file %s " % file_name
        code = None
        with open(file_name) as f:
            code = f.read()
        
        m = pattern_c.match(code);
        if m and m.group(1):
            headerless_code = re.sub(pattern_c, r'', code, 1) # replace first occurence
            print "Found C style header"
            new_code = header + headerless_code
            with open(file_name, "w") as output:
                output.write(new_code)
            continue
        
        else:    
            lines = None
            with open(file_name) as f:
                lines = f.readlines()

            existing_header_begin = 0
            existing_header_end = 0
            inside_cpp_comment = False
            for index, line in enumerate(lines):
                if pattern_cpp.match(line):
                    if inside_cpp_comment:
                        #print "inside C++ comment"
                        continue
                    else:    
                        inside_cpp_comment = True
                        existing_header_begin = index
                        #print "found beginning of C++ comment"
                        continue
                else:
                    existing_header_end = index
                    print "Found C++ style header: ", existing_header_end - existing_header_begin, " lines \n",
                    break
            strip_lines = existing_header_end - existing_header_begin
            strip_lines_and_add_header(file_name, strip_lines, header)

if __name__ == "__main__":
    # execute only if run as a script
    main()
