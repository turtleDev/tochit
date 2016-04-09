#      Project-Tochit' - A program to deloy MCQ self assessment tests
#
#                Copyright (C) 2013 Saravjeet 'Aman' Singh
#
# This file is a part of Project-Tochit'
#
# Project-Tochit' is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Project-Tochit' is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#

#
#    checkdb.py - Standalone program to check errors in Database File
#

import sys
from os.path import isfile



#   One thing that you guys will notice here is
#   that I've skipped any/all comments in this 
#   module, mostly because it's kind of self 
#   explanatory. for most of the part, the programs
#   just checks if every [] and {} are match correctly
#   and report it's line. This module is intended to be used
#   separately , but if the need be, it might be modified to instead
#   return errors in a string so that another program can
#   report it , in anyway it would like to                          



def is_answers_index_correct(data, line):
    """is_answers_index_correct(data, line) -> Boolean
    checks if the answer is within correct index of 1-4 and returns
    False if it not, True otherwise  """

    block = False
    l = 1
    ans = ''
    for x in data :
                
        if x == '\n':
            l += 1
        if l != line:
            continue
        else:
            if x == '[':
                block = True
                continue
            if block == True and x == ']':
                try:                # In case there nothing in the a[] section
                    ans = int(ans)  # python will raise a ValueError exception
                    break           
                except ValueError:  #in case there IS a ValueError
                    ans = 0         #This can be anything execpt for 1-4
                    break           # break out of the loop, tada
                    
            if block == True:
                ans += x
                continue
            
    if ans < 1 or ans > 4:
        return False
    else:
        return True

def checkdb(data):   
    "checkdb(x) Checks x for error of semantics"
    
    block = False     
    section = False   
    opt_count = 0     
    line = 1          
    found_q = found_a = False
    
    error = False
    
    for x in data:
        if x == '{' and block == True:						
            print "line %d: Found a mis matched { !"%line
            error = True
            continue
			
        if x == '{' and block == False:
            block = True
            continue
			
        if section == False:
            if x == 'q' or x == 'Q':
                found_q = True
            elif x == 'o' or x == 'O' :
                opt_count += 1
            elif x == 'a' or x == 'A':
                found_a = True
                if not is_answers_index_correct(data, line):
                    print "Error! Answer is out of index of 1-4 at line %d"%line
                    error = True
		            
        if x == '[' and section == False:
            section = True
            continue
		
        if x == '[' and section == True:
            print "line %d: Found at mis matched [ !"%line
            error = True
            continue
			
        if x == ']' and section == True:
            section = False
            continue

    	if x == ']' and section == False:
            print "line %d: Found a mis matched ] !"%line
            error = True
            continue
			
        if x == '}' and block == False:
            print "line %d: found a mis matched } !"%line
            error = True
            continue

        if x == '}' and block == True:
            if found_q == True and found_a == True and opt_count == 4:
                found_q = found_a = False
                opt_count = 0
                block = False
                continue
            else:
                print "Missing question/answer/option in block",
                print "preceding line %d !"%line
                error = True
                found_q = found_a = False
                opt_count = 0
                block = False
                continue
	
        if x == '\n':
            line += 1
            continue		
			
    if error == False:
        print "\nNo Errors in DB were Found!"
		
		
if __name__ == '__main__':
    try:
        filename = raw_input("Enter the name of the file(Ctrl-C to Exit): ")
    except KeyboardInterrupt:
        raw_input('\n-----------------\nPress Enter To Exit')
        sys.exit(0)
    if isfile(filename) == True:
        f = open(filename)
        x = f.read()
        f.close()
        checkdb(x)
    else:
        print"Error! file not found!\n"
	
    print"\nPress enter to exit "
    raw_input()
