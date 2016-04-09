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
#          parse.py - parsing and allied functionaility module
#

import os


class question():  
	"""This class will hold all the data regarding a particular question"""

	
	def __init__(self, data):
	
		found_q = found_a = False
		found_o1 = found_o2 = found_o3 = found_o4 = False
		block = False
		i = 0
		x = data
		
		self.question = ''
		self.opt1 = ''
		self.opt2 = ''
		self.opt3 = ''
		self.opt4 = ''
		self.answer = 0
        
#     Okay now a lot of people are gonna flame me for doing 
#     all the initialisation here, with NO error checking.
#     The reason is because the program is aimed at providing limited
#     functionality of students being able to prepare for tests or for
#     teachers to have another way of conducting/deploying tests.If in the
#     future , the need arises, i'll add error checking. For the time being
#     there's a utility named checkdb in *folder*/bin/ that will help 
#     out with checking the Database text file for possible errors of 
#     semantics. Most of the users of this program won't be concerned 
#     with dbfile etc though.

		
		while(x[i] != '}'):
		
			if block == False:
				if x[i] == 'q' or x[i] == 'Q':
					found_q = True
				if x[i] == 'o' or x[i] == 'O':
					if x[i+1] == '1':
						found_o1 = True
					elif x[i+1] == '2':
						found_o2 = True
					elif x[i+1] == '3':
						found_o3 = True
					elif x[i+1] == '4':
						found_o4 = True
					
				if x[i] == 'a' or x[i] == 'A':
					found_a = True
				
			if x[i] == '[':
				block = True
				i += 1
				continue
			if x[i] == ']':
				block = False
				found_q = found_a = False
				found_o1 = found_o2 = found_o3 = found_o4 = False
				i += 1
				continue
			
			if found_q == True and block == True:
				while x[i] != ']':
					self.question += x[i]
					i += 1
				continue
			
		
			if found_o1 == True and block == True:
				while x[i] != ']':
					self.opt1 += x[i]
					i += 1
				continue
			if found_o2 == True and block == True:
				while x[i] != ']':
					self.opt2 += x[i]
					i += 1
				continue
			if found_o3 == True and block == True:
				while x[i] != ']':
					self.opt3 += x[i]
					i += 1
				continue
			if found_o4 == True and block == True:
				while x[i] != ']':
					self.opt4 += x[i]
					i += 1
				continue
				
				
				
			if found_a == True and block == True:
				while x[i] != ']':
					if x[i].isdigit() == True:
						self.answer = int(x[i])
					i += 1
				continue
			i += 1

def readfile(filename, identifier):
    """readfile(f, identifier) -> str
    Reads data from a file and returns a string contating such data
    or -1 for error\n. it first checks if the first line of the file
    contains *identifier*, if it does it will return that string otherwise
    it will just return -1"""
    
    fexists = os.path.isfile(filename)
    
    if fexists == False:
        return -1
    
    f = open(filename)
    data = f.read()
    f.close()
    
    if data[:len(identifier)] != identifier:
        return -1
    else:
        data = data[len(identifier):]
        return data
	
	
def parse(data):
	"""parse(x) -> list
	parse will extract data in x and initiate a list
	containing objects of question class, with 
	each object containing question, options and
	an answer attributes"""
	
	block = False
	x = ''
	l = []
	for i in data:
		if i == '{':
			block = True
		
		if block == True:
			x += i
		if i == '}':
			block = False
			l.append(question(x)) 
			x = ''
	return l
