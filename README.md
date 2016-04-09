# tochit

Project-Tochit' 
Version-1.093


What is Project-Tochit'?
--------------------------------------------------------------------------------
* Project Tochit' is a tool used to deploy self assessment tests to students.
  The test structure is in the form of Multi-Choice Questionaire. It was designed 
  with a view, of helping students for preparing for exams.

* `Tochit'` is russian for "to sharpen".


Usage
--------------------------------------------------------------------------------

* On windows:

  Go to win32 -> tochit.exe

* On nix's(for eg linux), just open up tochit.py. Most linuxs already have GTK
  on them. In case you don't have it, you will have to download it.

  
  
Where can i Find the Source?
--------------------------------------------------------------------------------
* Source Files are contained in the 'src' folder  



General Notes
--------------------------------------------------------------------------------

* This software is intended to be used by teachers to deploy Multiple Choice 
  Question Style Self-Assessment Tests.
  
* The Software let's you choose from a list of databases, select the the topic
  over which you'd like to self-assess. The software would then ask you the
  length of the test you'd like to give. Currently, you can give tests in the 
  lengths of 25, 50 and 100 Questions. A window will then appear telling you to
  wait for 5 seconds and the test will start. you can:
  1) click on an option to select it as your answer
  2) click again on an option you previously clicked to de-select it
  3) skip any question by not answering it
  
  At the last question, if you click 'next',you will be asked if you wish to see
  your result. If you click ok, you will be shown the result, if you click 'no',
  you can carry on with your test(make modifications or skip questions)
  
* The result window will show you the number of questions there were in total, 
  the number of question you attempted, the number of questions you answered 
  correctly, and the number of questions you answered incorrectly.
  
* You can click on 'introspect' button to check which questions you got right 
  and which questions you got wrong. The right answer will be shown by a green-
  tick and a wrong answer will be shown by red cross. if you got the answer 
  right or if you did not answer the questions, then no red-cross will be shown.
  For every answer that you did not attempt , a warning will appear at the 
  bottom of the window telling you that you did not attempt that question
  
* The test(s) have a time limit depending on the number of questions. Future
  version might have support to disable this feature or change the amout of
  time allotted per question.

How to Create a Database file
--------------------------------------------------------------------------------
* A Database file is simply a text file , which contains question data.
* Your Database file can be named to anything, but try and use .txt extension, 
  since when displaying the name of the database, it'll only strip .text from 
  the name, other formats will be ignored and displayed as is.
* the starting characters of the file must be "##db##"(without double quotes),
  if these characters are not present, then the file won't be parsed and will be
  ignored
* The format for writing a questions is contained in docs/format.txt file

* A question is contained in between two matching opening brace ( { ) and 
  closing brace( } ). every question will contain 1 question block, in the form
  of q[...] where anything between the starting square bracket ( [ ) and closing
  square bracket( ] ) will be parsed as the question. note that you can use 
  captial q (Q) as well.

* You can write options in the form of o#[...] , where # is the option number 
  and just like above, anything betwee [ and ] will be parsed as the option.
  you may use capital o (O) as well
  
* Answer is written as a[...]. This value must be a number between 1 to 4 
  signifying which option is the correct option. And just like above, you can
  use capital a (A) as well

* Be sure to copy your database file to both *root folder*/database/ and 
  *root folder*/win32/database/ , so that your redistributed copy can be used
  by windows user/linux users without python/gtk alike :)

Trouble Shooting
--------------------------------------------------------------------------------
* If you are using Windows, have python 2.7 and gtk+ runtime yet you can't run
  the .pyc/.pyw files, it may be because that the byte code of those file is no 
  longer compatible with the python release you use. The easiest way to fix this
  problem is to copy all sources from src and place them in the respective 
  places, then you can either use them like that, or you can byte compile them
  again.
  
  If you wish to byte-compile any of the modules, start up python by typing 
  python in command prompt(don't forget to first navigate to Project-Tochit'
  folder), type in import *module src name without py extension* (for eg import 
  tochit) and then press ctrl-z or type exit(). try checking the directory/
  folder, there should be a .pyc file there now, you can delete the .py file(
  since there already is one copy in src folder) and use this .pyc file.
  
  -> 'A Command Prompt/Terminal Appears when i use the new pyc file'
  A : Just rename your file from .pyc to .pyw and it won't appear anymore


* "When i click on 50 tests, only 25 questions appear with the 'Indian Contract
   act, 1872 ..."
   
   This is not a bug. That database only contains 25 questions to begin with.
   The way how project tochit' generates a new test is that it randomly chooses
   N number of questions from database, or if the selected length of the test is
   more than the available questions in database, then all the available
   questions are selected for test. In this case, the "Indian Contract Act, 1872"
   only ships with 25 questions, so selecting more questions in test length 
   window won't result in more than 25 questions appearing, Since that databse
   only holds 25 questions.
   
   

Author: Saravjeet 'Aman' Singh

E-Mail: saravjeetamansingh@gmail.com

License: GNU General Public License

Copyright (C) 2013-2014 Saravjeet 'Aman' Singh.

