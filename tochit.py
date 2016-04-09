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
#                tochit.py - core program module 
#

# Standard Library Imports

import sys
import os
import random
import time

# Program Specific Imports

from lib import parse as parser
from lib.timer import timer as new_timer

# Gtk Imports
try: 
    import pygtk
    pygtk.require('2.0')
    import gtk
    import gtk.glade
    import gobject
except:
    print "Error! Gtk, Gobject, PyGtk or Glade Import Failed"
    sys.exit(-1)

    
# Globals Declarations

Program_Version = '1.093'
    

### Graphical User Interface ###

    
class UI(object):

    def __init__(self):
    
        ### GtkBuilder Initialization ###
        
        interface_file = os.path.join("data","ui","interface.glade")
        wintree = gtk.Builder()
        wintree.add_from_file(interface_file)
        
        ### misc configuration ###
        
        default_ui_settings = gtk.settings_get_default()
        default_ui_settings.props.gtk_button_images = True

        self.test_is_active = False

        self.SECONDS_PER_QUESTION = 30
        
        global Program_Version
        
            
        ### mainwin ###
        
        self.mainwin = gtk.Window()
        self.mainwin.set_size_request(640, 480)
        self.mainwin.set_resizable(False)
        self.mainwin.set_position(gtk.WIN_POS_CENTER)
        self.mainwin.set_title("Project-Tochit'")
        self.mainwin.set_icon_from_file(
                        os.path.join("data","icons","application-x-executable.png"))
    
        mainwin_menu = gtk.MenuBar()
        mainwin_menu.set_size_request(-1, 25)
    
        mainwin_file = gtk.MenuItem("_File")
        mainwin_help = gtk.MenuItem("_Help")
    
        fmenu = gtk.Menu()
        hmenu = gtk.Menu()
    
        mainwin_file_newtest = gtk.MenuItem("_New Test")
        mainwin_file_sep = gtk.SeparatorMenuItem()
        mainwin_file_exit = gtk.MenuItem("E_xit")
    
        mainwin_help_about = gtk.MenuItem("_About")
    
        fmenu.append(mainwin_file_newtest)
        fmenu.append(mainwin_file_sep)
        fmenu.append(mainwin_file_exit)
    
        hmenu.append(mainwin_help_about)
    
        mainwin_file.set_submenu(fmenu)
        mainwin_help.set_submenu(hmenu)
    
        mainwin_menu.append(mainwin_file)
        mainwin_menu.append(mainwin_help)
    
        mainwin_img = gtk.Image()
    
        mainwin_statusbar = gtk.Statusbar()
        mainwin_statusbar.set_has_resize_grip(False)
    
        mainwin_vbox = gtk.VBox()
    
        mainwin_vbox.pack_start(mainwin_menu, False, False, 0)
        mainwin_vbox.pack_start(mainwin_img, True, False, 0)
        mainwin_vbox.pack_start(mainwin_statusbar, False, False, 0)
    
        self.mainwin.add(mainwin_vbox) 
        
        ### image setup  ###
        img_src = os.path.join("data","images")
        
        mainwin_img_src = os.path.join(os.getcwd(),img_src)
        
        mainwin_img_src_contents = os.listdir(mainwin_img_src)
        
        if len(mainwin_img_src_contents) != 0:

            # On windows, sometimes a file named 'thumbs.db' is automatically
            # created, and when this file is loaded as an image, a GLib 
            # exception is raised stating that it could not identify the
            # image type, _remove_thumbsdb() just removes this from this
            # list of files, if it exists 

            self._remove_thumbsdb(mainwin_img_src_contents)

            random.seed()
            
            mainwin_img_src_max = len(mainwin_img_src_contents)
            
            img = mainwin_img_src_contents[random.randint(
                                           0, mainwin_img_src_max -1)]
            
            mainwin_img_src = os.path.join(mainwin_img_src,img)
            pixelbuffer = gtk.gdk.pixbuf_new_from_file(
                                        mainwin_img_src)
            
            pf = pixelbuffer.scale_simple(640, 435, gtk.gdk.INTERP_HYPER)
           
            
            mainwin_img.set_from_pixbuf(pf)
            
        
        
           
        # note: if anyone has seen this program's glade file and are
        # wondering why i set this icon when it's already set in glade
        # file? well i had set this icon for other windows as well and 
        # i did that after quite a while from when i had first designed that 
        # glade file. I wanted to remove it from the glade file , but 
        # glade designer for some reason wasn't letting me clear the icon
        # field ,so i decided to add this here anyway just for the sake 
        # of it and to make the usage of this icon more 'global' 
        # in this module
               
        
        ### aboutwin ###
        
        self.aboutwin = gtk.Dialog("About Tochit'")
        
        self.aboutwin.set_size_request(300, 225)
        self.aboutwin.set_position(gtk.WIN_POS_CENTER)
        self.aboutwin.set_modal(True)
        self.aboutwin.set_resizable(False)
        self.aboutwin.set_icon_from_file(
                    os.path.join("data","icons","application-x-executable.png"))
        
        
        
        # I haven't explicitly shown the label using show() method
        # instead i used show_all() on it's parent, i.e. aboutwin
        
        
        aboutwinlabel = gtk.Label(
        "<span font='16'><b>Project-Tochit'</b></span>")   
        
        aboutwinlabel2 = gtk.Label(
        "<span font='10'><b>Version %s</b></span>"%Program_Version)
        
        aboutwinlabel3 = gtk.Label(
        "<span font='10'><b>Copyright (C) 2013-2014</b></span>")
        
        aboutwinlabel4 = gtk.Label(
        "<span font='10'><b>Author: Saravjeet 'Aman' Singh</b></span>")
            
        aboutwinlabel5 = gtk.Label(
        "<span font='10'><b>A Software to delpoy MCQ\
</b></span>")
        
        aboutwinlabel6 = gtk.Label(
        "<span font='10'><b>Self-Assessment Tests</b></span>")
        
        aboutwinpadding = gtk.Label()
        
        
        
        # This is to enable markup parsing by pango text library
        
        
        aboutwinlabel.set_use_markup(True)
        aboutwinlabel2.set_use_markup(True)
        aboutwinlabel3.set_use_markup(True)
        aboutwinlabel4.set_use_markup(True)
        aboutwinlabel5.set_use_markup(True)
        aboutwinlabel6.set_use_markup(True)
        
        self.aboutwin.vbox.pack_start(aboutwinlabel, False, False, 10)
        self.aboutwin.vbox.pack_start(aboutwinlabel2, False, False, 2)
        self.aboutwin.vbox.pack_start(aboutwinlabel3, False, False, 3)
        self.aboutwin.vbox.pack_start(aboutwinlabel4, False, False, 3)
        self.aboutwin.vbox.pack_start(aboutwinpadding, False, False, 3)
        self.aboutwin.vbox.pack_start(aboutwinlabel5, False, False, 0)
        self.aboutwin.vbox.pack_start(aboutwinlabel6, False, False, 0)
        
        
        aboutwin_ok = gtk.Button("Okay")
       
        self.aboutwin.action_area.pack_start(aboutwin_ok)
        self.aboutwin.set_skip_taskbar_hint(True)
        self.aboutwin.set_skip_pager_hint(True)
        
        ### pretestwin ###
        
        self.pretestwin = gtk.Dialog("Please Wait ...")
        self.pretestwin.set_size_request(640, 480)
        self.pretestwin.set_modal(True)
        self.pretestwin.set_resizable(False)
        self.pretestwin.set_deletable(False)
        self.pretestwin.set_position(gtk.WIN_POS_CENTER)
        self.pretestwin.set_icon_from_file(
                    os.path.join("data","icons","application-x-executable.png"))
        
        self.pretestwin_label = gtk.Label()
        
        self.pretestwin.vbox.pack_start(self.pretestwin_label, True, False, 0)
        
        ### testwin ###
        
        self.testwin = wintree.get_object("TestWin")
        self.testwin.set_icon_from_file(
                            os.path.join("data","icons","application-x-executable.png"))
        
        testwin_choice_1 = wintree.get_object("TestWin_Choice1")
        testwin_choice_2 = wintree.get_object("TestWin_Choice2")
        testwin_choice_3 = wintree.get_object("TestWin_Choice3")
        testwin_choice_4 = wintree.get_object("TestWin_Choice4")
        
        testwin_choice_none = gtk.RadioButton()
        
        testwin_choice_1.set_group(testwin_choice_none)
        testwin_choice_2.set_group(testwin_choice_none)
        testwin_choice_3.set_group(testwin_choice_none)
        testwin_choice_4.set_group(testwin_choice_none)
        
        question = wintree.get_object("TestWin_Question")
        option1 = wintree.get_object("TestWin_Option1")
        option2 = wintree.get_object("TestWin_Option2")
        option3 = wintree.get_object("TestWin_Option3")
        option4 = wintree.get_object("TestWin_Option4")
        
        # testwin_next has been setup as an attribute here.
        #
        # Because at later stages , it will be modified by other methods
        # take a look at _new_test() to get a better understanding why it 
        # has been declared as attributes as againt local variables
        
        testwin_status = wintree.get_object("TestWin_Status")
        self.testwin_back = wintree.get_object("TestWin_Back")
        testwin_next = wintree.get_object("TestWin_Next")
        testwin_exit = wintree.get_object("TestWin_Exit")
        
        # set image on these buttons
        
        testwin_back_img = gtk.Image()
        testwin_next_img = gtk.Image()
        
        testwin_back_img.set_from_file(
                        os.path.join("data","icons","back.png"))
        
        testwin_next_img.set_from_file(
                        os.path.join("data","icons","forward.png"))
        
        self.testwin_back.set_image(testwin_back_img)
        testwin_next.set_image(testwin_next_img)

        testwin_timer = wintree.get_object("TestWin_Timer")
        testwin_timer.set_use_markup(True)

                
        # here i've packed all the labels in testwin into a dictonary for 
        # convinence of use later 
        
        self.testwin_interface = {'que' : question, 'opt1' : option1,
                                  'opt2' : option2 , 'opt3' : option3,
                                  'opt4' : option4 ,
                                  'btn1' : testwin_choice_1,
                                  'btn2' : testwin_choice_2, 
                                  'btn3' : testwin_choice_3,
                                  'btn4' : testwin_choice_4,
                                  'btn0' : testwin_choice_none,
                                  'status':testwin_status,
                                  'timer':testwin_timer
                                  }
                                  
        ### timeoutwin ###

        # This is a dialog that appears when time runs out during a test

        self.timeoutwin = gtk.Dialog("Time's Up!")
        self.timeoutwin.set_size_request(500, 135)
        self.timeoutwin.set_position(gtk.WIN_POS_CENTER)
        self.timeoutwin.set_resizable(False)
        self.timeoutwin.set_modal(True)
        self.timeoutwin.set_icon_from_file(
                            os.path.join("data","icons","application-x-executable.png"))


        timeoutwin_img = gtk.Image()
        timeoutwin_img.set_from_file(os.path.join("data","icons","appointment.png"))


        timeoutwin_message_text = "Time for your test has run out.\n\
Please proceed to the end of the\n\
test to see your Result."

        timeoutwin_message = gtk.Label()
        timeoutwin_message.set_markup("<span font_family='monospace' font='12'>"
                        +timeoutwin_message_text+"</span>")

        timeoutwin_ok = gtk.Button("Okay")
        timeoutwin_ok.set_size_request(85, 35)

        timeoutwin_padding = gtk.Label()
        timeoutwin_padding2 = gtk.Label()
        timeoutwin_padding3 = gtk.Label()
        timeoutwin_padding4 = gtk.Label()

        timeoutwin_hbox = gtk.HBox()
        timeoutwin_hbox2 = gtk.HBox()
        timeoutwin_vbox = gtk.VBox()

        timeoutwin_hbox2.pack_end(timeoutwin_padding, False, False, 72)
        timeoutwin_hbox2.pack_end(timeoutwin_ok, False, False)

        timeoutwin_vbox.pack_start(timeoutwin_padding2, False, False, 1)
        timeoutwin_vbox.pack_start(timeoutwin_message, False, False)
        timeoutwin_vbox.pack_start(timeoutwin_padding3, False, False)
        timeoutwin_vbox.pack_start(timeoutwin_hbox2, False, False)

        timeoutwin_hbox.pack_start(timeoutwin_padding4, False, False, 25)
        timeoutwin_hbox.pack_start(timeoutwin_img, False, False)
        timeoutwin_hbox.pack_start(timeoutwin_vbox, True, False)

        self.timeoutwin.vbox.pack_start(timeoutwin_hbox, False, False)
        
        ### selectionwin ###
        
        
        # A gist of what's happening below, basically i setup 3 attributes
        # i.e. selectionwin, selectionwin_treeview and selectionwin_data
        # selectionwin_data is gonna be populated with a list of available db's
        # selectionwin_treeview is there so i can setup handlers and 
        # selectionwin being there is self explainatory
        
        
        self.selectionwin = gtk.Dialog("Select Database")
        self.selectionwin.set_size_request(250, 300)
        self.selectionwin.set_resizable(False)
        self.selectionwin.set_modal(True)
        self.selectionwin.set_position(gtk.WIN_POS_CENTER)
        self.selectionwin.set_icon_from_file(
                    os.path.join("data","icons","application-x-executable.png"))
        
        self.selectionwin_data = gtk.ListStore(str)
        
        self.selectionwin_treeview = gtk.TreeView(self.selectionwin_data)
        
        selectionwin_cellrenderer = gtk.CellRendererText()
        
        
        selectionwin_scrolledwin = gtk.ScrolledWindow()
        selectionwin_scrolledwin.set_policy(gtk.POLICY_AUTOMATIC,
                                            gtk.POLICY_AUTOMATIC)
        
        
        selectionwin_column = gtk.TreeViewColumn("Available Database(s)")
        selectionwin_column.pack_start(selectionwin_cellrenderer, True)
        selectionwin_column.add_attribute(selectionwin_cellrenderer, 'text', 0)
        
        
        self.selectionwin_treeview.append_column(selectionwin_column)
        
        selectionwin_scrolledwin.add_with_viewport(self.selectionwin_treeview)
        
        self.selectionwin.vbox.pack_start(selectionwin_scrolledwin)
        
        selectionwin_ok = gtk.Button("Ok")
        selectionwin_cancel = gtk.Button("Cancel")
        
        # IMPORTANT NOTE: selectionwin_ok button is not an attribute of this 
        # class. When setting up signal handler for this button, pass the 
        # selectionwin as argument so that you can retrieve which row is 
        # highlighted
        
        selectionwin_ok.set_size_request(72, 30)
        selectionwin_cancel.set_size_request(72, 30)
        
        
        selectionwin_hbox = gtk.HBox(True)
        
        selectionwin_hbox.pack_start(selectionwin_cancel, True, False , 0)
        selectionwin_hbox.pack_start(selectionwin_ok, True, False , 0)
        
        self.selectionwin.vbox.pack_start(selectionwin_hbox, False, False, 4)
        
        ### testlengthwin ###
        
        # This win will appear immediately after the user has selected the db
        # of his choice in selectionwin, and then will select the length of the
        # test. 
        #
        # NOTE: if the database has insufficient questions, then test length 
        #       will be limited to only those questions
        
        self.testlengthwin = gtk.Dialog("Select Test Length")
        self.testlengthwin.set_size_request(250, 300)
        self.testlengthwin.set_resizable(False)
        self.testlengthwin.set_position(gtk.WIN_POS_CENTER)
        self.testlengthwin.set_modal(True)
        self.testlengthwin.set_icon_from_file(
                    os.path.join("data","icons","application-x-executable.png"))
        
        
        testlengthwin_25q = gtk.Button("25 Questions")
        testlengthwin_50q = gtk.Button("50 Questions")
        testlengthwin_100q = gtk.Button("100 Questions")
        
        testlengthwin_25q.set_size_request(-1, 65)
        testlengthwin_50q.set_size_request(-1, 65)
        testlengthwin_100q.set_size_request(-1, 65)
        
        self.testlengthwin.vbox.pack_start(testlengthwin_25q, True, False, 0)
        self.testlengthwin.vbox.pack_start(testlengthwin_50q, True, False, 0)
        self.testlengthwin.vbox.pack_start(testlengthwin_100q, True, False, 0)
        
        
        ### testwin_confirm_end  ###
        
        self.testwin_confirm_end = gtk.Dialog("Are You Sure??")
        self.testwin_confirm_end.set_size_request(500, 135)
        self.testwin_confirm_end.set_resizable(False)
        self.testwin_confirm_end.set_modal(True)
        self.testwin_confirm_end.set_position(gtk.WIN_POS_CENTER)
        self.testwin_confirm_end.set_icon_from_file(
                os.path.join("data","icons","application-x-executable.png"))
        
        testwin_confirm_end_yes = gtk.Button("Yes")
        testwin_confirm_end_no = gtk.Button("No")
        
        testwin_padding = gtk.Label()
        testwin_padding2 = gtk.Label()
        
        testwin_confirm_end_yes.set_size_request(70, 30)
        testwin_confirm_end_no.set_size_request(70, 30)
        
        testwin_message = gtk.Label(
            "<span font='12' font_family='monospace'>\
You have reached the end of this Test</span>")

        testwin_message2= gtk.Label(
        "<span font='12' font_family='monospace'>\
Do you wish to see the result?</span>")
        
        testwin_message.set_use_markup(True)
        testwin_message2.set_use_markup(True)
        
        self.testwin_confirm_end.remove(self.testwin_confirm_end.vbox)
    
        testwin_confirm_end_hbox = gtk.HBox(False)
        testwin_confirm_end_vbox = gtk.VBox(False)
        testwin_confirm_end_hbox2 = gtk.HBox(False)
        
                
        img = gtk.Image()
        img.set_from_file(os.path.join("data","icons","ascii.png"))
        
        testwin_confirm_end_hbox.pack_start(img, False, False, 35)
        testwin_confirm_end_hbox.pack_start(testwin_confirm_end_vbox, False, 
                                                                        False)
                                                                        
        testwin_confirm_end_vbox.pack_start(testwin_message, False, False, 15)
        testwin_confirm_end_vbox.pack_start(testwin_message2, False, False, 0)
        
        testwin_confirm_end_vbox.pack_start(testwin_padding2, False, False, 1)
        
        testwin_confirm_end_vbox.pack_start(testwin_confirm_end_hbox2, False,
                                                                False, )
        testwin_confirm_end_hbox2.pack_end(testwin_padding, False, False, 50)
        testwin_confirm_end_hbox2.pack_end(testwin_confirm_end_no, False, False,
                                                                              0)
        testwin_confirm_end_hbox2.pack_end(testwin_confirm_end_yes, False, False
                                                                           , 11)
        
        self.testwin_confirm_end.add(testwin_confirm_end_hbox)        
        
        
        ### msg db empty ###
        
        self.msg_db_empty = gtk.Dialog("Empty Database")
        self.msg_db_empty.set_position(gtk.WIN_POS_CENTER)
        self.msg_db_empty.set_size_request(500, 145)
        self.msg_db_empty.set_resizable(False)
        self.msg_db_empty.set_icon_from_file(
                os.path.join("data","icons","application-x-executable.png"))
                
        msg_db_empty_ok = gtk.Button("Okay")
        msg_db_empty_ok.set_size_request(80, 30)
        
        # the message in the dialog is set in _msg_db_empty_show() method
        self.msg_db_empty_data = gtk.Label()
        
        msg_db_empty_hbox = gtk.HBox()
        
        self.msg_db_empty.vbox.pack_start(self.msg_db_empty_data, True, False,0)
        msg_db_empty_hbox.pack_start(msg_db_empty_ok, True, False,0)
        
        self.msg_db_empty.vbox.pack_start(msg_db_empty_hbox, False, False, 0)
        
        
        ### resultwin ###
        
        self.resultwin = gtk.Window()
        self.resultwin.set_title('Results')
        self.resultwin.set_size_request(640, 480)
        self.resultwin.set_resizable(False)
        self.resultwin.set_position(gtk.WIN_POS_CENTER)
        self.resultwin.set_icon_from_file(
                            os.path.join("data","icons","application-x-executable.png"))
        
        resultwin_img = gtk.Image()
        resultwin_img.set_from_file(os.path.join("data","icons","stock_paste.png"))
        
        self.resultwin_text = gtk.Label()
       
        resultwin_exit_img = gtk.Image()
        resultwin_exit_img.set_from_file(os.path.join("data","icons","exit.png"))
        
        resultwin_introspect_img = gtk.Image()
        resultwin_introspect_img.set_from_file(os.path.join("data","icons","document_new.png"))
        
        resultwin_introspect = gtk.Button("Introspect")
        resultwin_exit = gtk.Button("Exit")
        
        resultwin_introspect.set_size_request(100, 45)
        resultwin_exit.set_size_request(100, 45)
        
        resultwin_hsep = gtk.HSeparator()
        
        resultwin_padding = gtk.Label()
        resultwin_padding2 = gtk.Label()
        
        resultwin_introspect.set_image(resultwin_introspect_img)
        resultwin_exit.set_image(resultwin_exit_img)
        
        resultwin_introspect.set_image_position(gtk.POS_RIGHT)
        resultwin_exit.set_image_position(gtk.POS_LEFT)
        
        resultwin_vbox = gtk.VBox()
        
        resultwin_hbox = gtk.HBox()
        
        resultwin_vbox.pack_start(resultwin_img, False, False, 50)
        
        resultwin_vbox.pack_start(self.resultwin_text, True, False, 0)
        
        resultwin_vbox.pack_start(resultwin_padding, False, False, 25)
        
        resultwin_vbox.pack_start(resultwin_hsep, False, False, 5)
        
        
        resultwin_vbox.pack_start(resultwin_hbox, False, False, 10)
        
        resultwin_vbox.pack_start(resultwin_padding2, False, False, 5)
        
        
        resultwin_hbox.pack_start(resultwin_introspect, False, False, 75)
        resultwin_hbox.pack_end(resultwin_exit, False, False, 75)
        
        self.resultwin.add(resultwin_vbox)
        
        ### testwin_confirm_quit ###
        
        self.testwin_confirm_quit = gtk.Dialog("Confirm Exit")
        self.testwin_confirm_quit.set_size_request(500, 135)
        self.testwin_confirm_quit.set_modal(True)
        self.testwin_confirm_quit.set_resizable(False)
        self.testwin_confirm_quit.set_position(gtk.WIN_POS_CENTER)
        self.testwin_confirm_quit.set_icon_from_file(
                            os.path.join("data","icons","application-x-executable.png"))
        
        testwin_confirm_quit_text1 =gtk.Label("\
<span font_family='monospace' font='13'>The Test is still in Progress</span>")
        
        testwin_confirm_quit_text1.set_use_markup(True)
        
        testwin_confirm_quit_text2 =gtk.Label("\
<span font_family='monospace' font='13'>Do You Wish To Exit?</span>")
        testwin_confirm_quit_text2.set_use_markup(True)
        
        
        testwin_confirm_quit_hbox = gtk.HBox()
        testwin_confirm_quit_hbox2 = gtk.HBox()
        testwin_confirm_quit_vbox2 = gtk.VBox()
        
        testwin_confirm_quit_yes = gtk.Button("Yes")
        testwin_confirm_quit_yes.set_size_request(70, 30)
        
        testwin_confirm_quit_no = gtk.Button("No")
        testwin_confirm_quit_no.set_size_request(70, 30)
        
        testwin_confirm_quit_padding = gtk.Label()
        testwin_confirm_quit_padding2 = gtk.Label()
        
        testwin_confirm_quit_img = gtk.Image()
        testwin_confirm_quit_img.set_from_file(
                            os.path.join("data","icons","ascii.png"))
                            
        testwin_confirm_quit_vbox2.pack_start(testwin_confirm_quit_padding2,
                                                False, False, 2)
        
        testwin_confirm_quit_vbox2.pack_start(testwin_confirm_quit_text1,
                                                False, False, 3)
                                                
        testwin_confirm_quit_vbox2.pack_start(testwin_confirm_quit_text2,
                                                False, False, 5)
                                                
        testwin_confirm_quit_vbox2.pack_start(testwin_confirm_quit_hbox,
                                                False, False, 10)
                                                
        
        testwin_confirm_quit_hbox.pack_start(testwin_confirm_quit_padding,
                                                False, False, 20)
                                                
        testwin_confirm_quit_hbox.pack_start(testwin_confirm_quit_yes,
                                                False, False, 5)
                                                
        testwin_confirm_quit_hbox.pack_start(testwin_confirm_quit_no,
                                                False, False, 5)
                                                
        testwin_confirm_quit_hbox2.pack_start(testwin_confirm_quit_img,
                                                False, False, 35)
                                                
        testwin_confirm_quit_hbox2.pack_start(testwin_confirm_quit_vbox2,
                                                False, False, 38)
        
        self.testwin_confirm_quit.vbox.pack_start(testwin_confirm_quit_hbox2,
                                                False, False, 0)
        
        
                                               
        
        ### Check Result Window ###
        
        self.checkresultwin = wintree.get_object("CheckResultWin")
        self.checkresultwin.set_icon_from_file(
                                    os.path.join("data","icons","application-x-executable.png"))
        self.checkresultwin.set_title("Results")                            
        
        checkresultwin_ic1 = wintree.get_object("CRW_ic1")
        checkresultwin_ic2 = wintree.get_object("CRW_ic2")
        checkresultwin_ic3 = wintree.get_object("CRW_ic3")
        checkresultwin_ic4 = wintree.get_object("CRW_ic4")
        
        checkresultwin_ic1.set_from_file(
                                os.path.join("data","icons","gtk_cancel.png"))
                                
        checkresultwin_ic2.set_from_file(
                                os.path.join("data","icons","gtk_cancel.png"))
                                
        checkresultwin_ic3.set_from_file(
                                os.path.join("data","icons","gtk_cancel.png"))
                                
        checkresultwin_ic4.set_from_file(
                                os.path.join("data","icons","gtk_cancel.png"))
                                
        checkresultwin_c1 = wintree.get_object("CRW_c1")
        checkresultwin_c2 = wintree.get_object("CRW_c2")
        checkresultwin_c3 = wintree.get_object("CRW_c3")
        checkresultwin_c4 = wintree.get_object("CRW_c4")
        
        checkresultwin_c1.set_from_file(
                                os.path.join("data","icons","tick_green.png"))
                                
        checkresultwin_c2.set_from_file(
                                os.path.join("data","icons","tick_green.png"))
                                
        checkresultwin_c3.set_from_file(
                                os.path.join("data","icons","tick_green.png"))
                                
        checkresultwin_c4.set_from_file(
                                os.path.join("data","icons","tick_green.png"))
                                
        
        self.checkresultwin_next = wintree.get_object(
                                "CheckResultWin_Next")
                                
        self.checkresultwin_back = wintree.get_object(
                                "CheckResultWin_Back")
                                
        checkresultwin_next_img = gtk.Image()
        checkresultwin_back_img = gtk.Image()
        
        checkresultwin_next_img.set_from_file(os.path.join("data","icons","forward.png"))
        checkresultwin_back_img.set_from_file(os.path.join("data","icons","back.png"))
        
        self.checkresultwin_next.set_image(checkresultwin_next_img)
        self.checkresultwin_back.set_image(checkresultwin_back_img)
        
        checkresultwin_exit = wintree.get_object(
                                "CheckResultWin_Exit")
                              
                              
        checkresultwin_question = wintree.get_object(
                                "CheckResultWin_Question")
        
        checkresultwin_opt1 = wintree.get_object("CheckResultWin_Option1")
        checkresultwin_opt2 = wintree.get_object("CheckResultWin_Option2")
        checkresultwin_opt3 = wintree.get_object("CheckResultWin_Option3")
        checkresultwin_opt4 = wintree.get_object("CheckResultWin_Option4")
        
        checkresultwin_status = wintree.get_object(
                                    "CheckResultWin_Status")

        checkresultwin_status_info = wintree.get_object("CheckResultWin_Status_Info")
        
        checkresultwin_status_info.set_label("")


        
        self.checkresultwin_interface = {   'que':checkresultwin_question,
                                            'opt1':checkresultwin_opt1,
                                            'opt2':checkresultwin_opt2,
                                            'opt3':checkresultwin_opt3,
                                            'opt4':checkresultwin_opt4,
                                            'c1':checkresultwin_c1,
                                            'c2':checkresultwin_c2,
                                            'c3':checkresultwin_c3,
                                            'c4':checkresultwin_c4,
                                            'ic1':checkresultwin_ic1,
                                            'ic2':checkresultwin_ic2,
                                            'ic3':checkresultwin_ic3,
                                            'ic4':checkresultwin_ic4,
                                            'status':checkresultwin_status,
                                            'status_info':checkresultwin_status_info
                                            
                                        }
                                        
        self.checkresultwin_interface['c1'].set_no_show_all(True)
        self.checkresultwin_interface['c2'].set_no_show_all(True)
        self.checkresultwin_interface['c3'].set_no_show_all(True)
        self.checkresultwin_interface['c4'].set_no_show_all(True)
        
        self.checkresultwin_interface['ic1'].set_no_show_all(True)
        self.checkresultwin_interface['ic2'].set_no_show_all(True)
        self.checkresultwin_interface['ic3'].set_no_show_all(True)
        self.checkresultwin_interface['ic4'].set_no_show_all(True)

                
        
        ### Callback's Setup ###
        # manual setup of signal handlers
        
        self.mainwin.connect("delete_event", gtk.main_quit)
        
        mainwin_file_exit.connect("activate", gtk.main_quit)
        
        mainwin_file_newtest.connect("activate", self._file_new)
        
        mainwin_help_about.connect("activate", self._help_about)
        
        self.testwin.connect("delete_event", self._testwin_confirm_quit_show)
        
        self.aboutwin.connect("delete_event", self._help_about_destroy)
        
        aboutwin_ok.connect("clicked", self._help_about_okay,
                                                self.aboutwin)
                                                
        self.selectionwin.connect("delete_event", self._selectionwin_destroy)
        
        selectionwin_ok.connect("clicked", self._selectionwin_ok_click)
        
        selectionwin_cancel.connect("clicked", self._selectionwin_cancel_click,
                                              self.selectionwin)
                                              
        self.selectionwin.connect("delete_event", self._selectionwin_destroy)
        
        self.selectionwin_treeview.connect("row_activated", 
                                            self._selectionwin_row_activated)
        
        testlengthwin_25q.connect("clicked", self._testlengthwin_button_clicked,
                                                                            25)
                                                                            
        testlengthwin_50q.connect("clicked", self._testlengthwin_button_clicked,
                                                                            50)
                                                                            
        testlengthwin_100q.connect("clicked", self._testlengthwin_button_clicked
                                                                           ,100)
        
        self.testlengthwin.connect("delete_event", self._testlengthwin_destroy)
                                                                           
        
        
        testwin_exit.connect("clicked", self._testwin_confirm_quit_show)
        
        testwin_next.connect("clicked", self._testwin_next)
        
        self.testwin_back.connect("clicked", self._testwin_back)
        
        self.testwin_confirm_end.connect("delete_event",
                                         self._testwin_confirm_end_no_clicked)
        
        testwin_confirm_end_yes.connect("clicked", 
                                        self._testwin_confirm_end_yes_clicked)
                                    
        testwin_confirm_end_no.connect("clicked", 
                                       self._testwin_confirm_end_no_clicked)
                                       
        self.msg_db_empty.connect("delete_event",
                                        self._msg_db_empty_ok_clicked)
        
        msg_db_empty_ok.connect("clicked", self._msg_db_empty_ok_clicked)
        
        self.resultwin.connect("delete_event", self._resultwin_exit)
        
        resultwin_exit.connect("clicked", self._resultwin_exit)
        
        self.testwin_confirm_quit.connect("delete_event",
                                        self._testwin_confirm_quit_no_clicked)
        
        testwin_confirm_quit_yes.connect("clicked",
                                        self._testwin_confirm_quit_yes_clicked)
                                        
        testwin_confirm_quit_no.connect("clicked",
                                        self._testwin_confirm_quit_no_clicked)
        
        resultwin_introspect.connect("clicked",
                                        self._checkresultwin_show)
                                        
        self.checkresultwin.connect("delete_event", self._checkresultwin_hide)
        
        checkresultwin_exit.connect("clicked", self._checkresultwin_hide)
                                        
        self.checkresultwin_next.connect("clicked",
                                                self._checkresultwin_next)
                                                
        self.checkresultwin_back.connect("clicked",
                                                self._checkresultwin_back)

        self.timeoutwin.connect("delete_event", self._timeoutwin_hide)

        timeoutwin_ok.connect("clicked", self._timeoutwin_hide)

        
                    
        h1 = self.testwin_interface['btn1'].connect(
                    "clicked", self._testwin_btn_clicked, 1)
                    
        h2 = self.testwin_interface['btn2'].connect(
                    "clicked", self._testwin_btn_clicked, 2)
                    
        h3 = self.testwin_interface['btn3'].connect(
                    "clicked", self._testwin_btn_clicked, 3)
                    
        h4 = self.testwin_interface['btn4'].connect(
                    "clicked", self._testwin_btn_clicked, 4)
                    
        # these handler id's will be used to temporarily
        # disable/enable signal handlers, check
        # _testwin_disable_handlers() and _testwin_enable_handlers()
        # for more info
        
        self.testwin_handlers = {'btn1' : h1, 'btn2' : h2,
                                 'btn3' : h3, 'btn4' : h4}
                    
        
        ### End of init()  ###
    
    ### Internal Interfaces ###
    
    def _help_about(self, widget, data=None):
        self.aboutwin.show_all()
        
    def _help_about_okay(self, widget , win):
        win.hide()
       
        
    # Instead of using the normal "destroy" signal , i've instead used
    # delete-event , because using destroy here would mean that window manager
    # would delete the widget inside the window and next time it's opened
    # it would just show an empty window, using delete-event let's us 
    # handle the destruction , which we don't do at all and just return True 
    # to tell window manager that we're done with the window and no further
    # 'handling' is required
    
    def _help_about_destroy(self, widget, event, data = None):
        widget.hide()
        return True
    
    def _selectionwin_destroy(self, widget, event, data=None):
        widget.hide()
        return True
    
    def _selectionwin_cancel_click(self, widget, win):
        win.hide()
        
    def _selectionwin_ok_click(self, widget, data=None):
        cursor = self.selectionwin_treeview.get_cursor()
        
        # the path returned by gtk.TreeView.get_cursor is in the format of 
        # ((x,y), y) , where the inner tuple shows the path to the currently
        # highlighted cell and the second y shows the column it belongs to
        # since our selection dialog(selectionwin) only consists of a single
        # column, we only need the x coordinate to know which row was activated

        
        try:                    # In case the user clicks on "ok" button    
            path = cursor[0][0] # when there is no available databases
        except TypeError:       # , The interpreter raises a TypeError.
            return              # Here, the functions execution stops
                                # at this point if the list is empty
        
        db_names = []
        
        for db in self.database:
            db_names.append(db[0])
            
        self.selection = db_names[path]
        
        self.selectionwin.hide()
        
        self.testlengthwin.show_all()
        
    def _selectionwin_row_activated(self , widget, path, view_column, data=None):
        # the path argument given by gtk signal system is in the form of
        # (x, y) and since our selection dialog(selectionwin) only consists of 
        # a single column , we only need the x coordinate to know which row was
        # activated.
        
        path = path[0]
        
        db_names = []
        
        for db in self.database:
            db_names.append(db[0])
        
        self.selection = db_names[path] # Clean this up after the test
        
        self.selectionwin.hide()
        
        self.testlengthwin.show_all()
        
    def _testlengthwin_button_clicked(self, widget, length):
        self.mainwin.hide()
        self.testlengthwin.hide()
        
        self._new_test(length)
        
    def _testlengthwin_destroy(self, widget, event, data=None):
        self.selection = None
        
        widget.hide()
        return True
    
    def _file_new(self, widget, data=None):
        self.selectionwin.show_all()
    
    
    def _generate_test(self, database, length):
    
        random.seed()
        
        if len(database) < length:
            length = len(database)
            
        y = list(database)          # make a copy of the original database
        x = list()                  # empty list to be returned
        
        while length != 0:
            
            index = random.randint(0, length-1)
            x.append([y.pop(index), 0])
            length = length -1
            
        return x    
    
    # _testwin_confirm_end_yes_clicked and _testwin_confirm_end_no_clicked
    # either stop the test by calling _result() method or continue the test
    # by the hiding the confirmation dialog itself
    
    def _testwin_confirm_end_yes_clicked(self, widget, data=None):
        self.testwin_confirm_end.hide()
        self.testwin.hide()
        self._result()
    
    # This might also be called by the window's "delete_event" signal    
    def _testwin_confirm_end_no_clicked(self, widget, data=None):
        self.testwin_confirm_end.hide()
        return True
    
    def _testwin_confirm_quit_yes_clicked(self, widget, data=None):
        self.testwin_confirm_quit.hide()
        self._stop_test()
        
    
    # This might also be called by the window's "delete_event" signal
    def _testwin_confirm_quit_no_clicked(self, widget, data=None):
        self.testwin_confirm_quit.hide()
        return True
    
    # Also might be called by testwin window's "destroy_event" signal
    def _testwin_confirm_quit_show(self, widget, data=None):
        self.testwin_confirm_quit.show_all()
        return True
    
    # _testwin_update() is used whenever any part of the program wants to 
    # update labels and buttons of testwin , using current_test and 
    # current_test_pos
    
    def _testwin_update(self):
        
        self._testwin_disable_handlers()
        
        self.testwin_interface['btn0'].emit("clicked")
        
        self._testwin_enable_handlers()
        
        que = self.current_test[self.current_test_pos][0].question
        o1 = self.current_test[self.current_test_pos][0].opt1
        o2 = self.current_test[self.current_test_pos][0].opt2
        o3 = self.current_test[self.current_test_pos][0].opt3
        o4 = self.current_test[self.current_test_pos][0].opt4
        
        self.testwin_interface['que'].set_markup(
                          "<span font_family='monospace' font='12'><b>"+que+"</b></span>")
        self.testwin_interface['opt1'].set_markup(
                                "<span font_family='monospace' font='12'>"+o1+"</span>")
        self.testwin_interface['opt2'].set_markup(
                                "<span font_family='monospace' font='12'>"+o2+"</span>")
        self.testwin_interface['opt3'].set_markup(
                                "<span font_family='monospace' font='12'>"+o3+"</span>")
        self.testwin_interface['opt4'].set_markup(
                                "<span font_family='monospace'font='12'>"+o4+"</span>")
        
        # +1 is added to current_test_pos as current_test_pos in itself is used
        # as an index(e.g. look above)
        
        self.testwin_interface['status'].set_label(
                                    "%d/%d"%(
                                         self.current_test_pos +1,
                                         self.current_test_max   ))
                                       
        # check if the user had answered a question previously and if so, 
        # high-light that answer for the user
        
        self._testwin_disable_handlers()
        
        btn = "btn%d"%self.current_test[self.current_test_pos][1]
        self.testwin_interface[btn].emit("clicked")
            
        self._testwin_enable_handlers()
        
        # forcefully redraw all visible widgets
        
        while gtk.events_pending():
            gtk.main_iteration_do(True)
    
    def _testwin_next(self, widget):
        self.current_test_pos = self.current_test_pos +1
        
        
        if self.current_test_pos == self.current_test_max:
            self.current_test_pos = self.current_test_pos -1
            self.testwin_confirm_end.show_all()
            return None
            
        if not self.testwin_back.get_sensitive():
            self.testwin_back.set_sensitive(True)
        
        self._testwin_update()
        
    def _testwin_back(self, widget):
        self.current_test_pos = self.current_test_pos -1
        
        if self.current_test_pos == 0:       # If current_test_pos is 0
            self.testwin_back.set_sensitive(False)
        
            
        self._testwin_update()
        
     
    def _testwin_btn_clicked(self, widget, new_answer):
    
        # if the callback was called with no new_answer arg , do nothing
        if new_answer == None:
            return 
            
        current_answer = self.current_test[self.current_test_pos][1]
        
        self._testwin_disable_handlers()
        
                                        
        if new_answer == current_answer:
            self.current_test[self.current_test_pos][1] = 0
            self.testwin_interface['btn0'].emit("clicked")
        else:
            self.current_test[self.current_test_pos][1] = new_answer
            widget.emit("clicked")
        
        
        
        self._testwin_enable_handlers()
                            
                            
    # _testwin_disable_handlers() and _testwin_enable_handlers() block or 
    # unblock signal handlers for radio buttons on testwin. Read detail below
    # as to the need of these two method.(optional)
    #
    #
    #
    # DETAILS: It is intended for the user to be able to 'mark-off' his answer
    # in case he accidently clicks an option, but doesn't not want to attempt 
    # that question. This was implemented by emitting a 'clicked' signal on 
    # the ghost button(the self.testwin_interface['btn0']), but this results
    # in an unwated behavior. This unwanted behaviour is that whenever a radio
    # button in a group is clicked, any other previously active button also 
    # emits a 'clicked' signal. To put it simply, the radio button widget emits
    # the 'clicked' signal when it is 'realeased', either by user or by the 
    # program itself. When ever the ghost button was clicked for a new question
    # or when another option was selected while one of the other radio buttons
    # were 'active' , it would result in recursive calls to the handlers 
    # resulting in ghost button getting clicked and result being set to 0
    # .The major reason for doing this though, is because the signal handlers of
    # these radio buttons also handle user's input. They manipulate the 
    # self.current_test to save the answer(in the second field), 
    # and whenever the ghost button was activated, it would set the answer for
    # that option to 0(not answered). look at _testwin_update() and _new_test()
    # to see how these two methods are used. 
    #
    # WARNING: These two methods do not check if the handlers were previously
    # disabled or enabled. Always use these two methods together. If 
    # _testwin_enable_handlers() is called when handlers are already enabled or
    # if _testwin_disable_handlers() is called when handlers are disabled, it 
    # might result in ugly GTK error(s). 
    
    def _testwin_disable_handlers(self):
    
        self.testwin_interface['btn1'].handler_block(
                                self.testwin_handlers['btn1'])
        
        self.testwin_interface['btn2'].handler_block(
                                self.testwin_handlers['btn2'])
        
        self.testwin_interface['btn3'].handler_block(
                                self.testwin_handlers['btn3'])
        
        self.testwin_interface['btn4'].handler_block(
                                self.testwin_handlers['btn4'])
        
    def _testwin_enable_handlers(self):
        
        self.testwin_interface['btn1'].handler_unblock(
                            self.testwin_handlers['btn1'])
        
        self.testwin_interface['btn2'].handler_unblock(
                            self.testwin_handlers['btn2'])
        
        self.testwin_interface['btn3'].handler_unblock(
                            self.testwin_handlers['btn3'])
        
        self.testwin_interface['btn4'].handler_unblock(
                            self.testwin_handlers['btn4'])



    # _testwin_disable_radiobuttons() and _testwin_enable_radiobuttons() 
    # disable/enable the radio buttons on testwindow. In contrast to 
    # _testwin_enable_handlers() / _testwin_disable_handlers(), these
    # two methods don't disable the signal handling for these buttons, 
    # they just make these buttons unreponsive to user actions (i.e
    # the buttons appear 'disabled' and they won't work when you click
    # on them). These will be used by timer to disable buttons when the
    # the time runs out during a test

    def _testwin_disable_radiobuttons(self):

        self.testwin_interface['btn1'].set_sensitive(False)
        self.testwin_interface['btn2'].set_sensitive(False)
        self.testwin_interface['btn3'].set_sensitive(False)
        self.testwin_interface['btn4'].set_sensitive(False)


    def _testwin_enable_radiobuttons(self):
        
        self.testwin_interface['btn1'].set_sensitive(True)
        self.testwin_interface['btn2'].set_sensitive(True)
        self.testwin_interface['btn3'].set_sensitive(True)
        self.testwin_interface['btn4'].set_sensitive(True)


    def _timeoutwin_hide(self, widget, data=None):

        self.timeoutwin.hide()

        # To stop further event handling in
        # case of "delete-event"
        return True

                            
                            
        
    def _checkresultwin_show(self, widget ,data=None):
        self.resultwin.hide()
        
        self.current_test_pos = 0
        self.checkresultwin_back.set_sensitive(False)

        self._checkresultwin_update()
        
        
        self.checkresultwin.show_all()
    
    def _checkresultwin_hide(self, widget, data=None):
        self.checkresultwin.hide()
        
        self.resultwin.show_all()
        return True # since this might be called by the window's "delete"
        
    
    def _checkresultwin_update(self):
    
        que = self.current_test[self.current_test_pos][0].question
        o1 = self.current_test[self.current_test_pos][0].opt1
        o2 = self.current_test[self.current_test_pos][0].opt2
        o3 = self.current_test[self.current_test_pos][0].opt3
        o4 = self.current_test[self.current_test_pos][0].opt4
        
        self.checkresultwin_interface['que'].set_markup(
                          "<span font_family='monospace' font='12'><b>"+que+"</b></span>")
        self.checkresultwin_interface['opt1'].set_markup(
                                "<span font_family='monospace' font='12'>"+o1+"</span>")
        self.checkresultwin_interface['opt2'].set_markup(
                                "<span font_family='monospace' font='12'>"+o2+"</span>")
        self.checkresultwin_interface['opt3'].set_markup(
                                "<span font_family='monospace' font='12'>"+o3+"</span>")
        self.checkresultwin_interface['opt4'].set_markup(
                                "<span font_family='monospace' font='12'>"+o4+"</span>")
                                
        
        #+1 is added to self.current_test_pos since it is used as a index
        self.checkresultwin_interface['status'].set_label(
                                    "%d/%d"%(self.current_test_pos +1,  
                                             self.current_test_max))
        
        #hide all icons
        
        self.checkresultwin_interface['c1'].hide()
        self.checkresultwin_interface['c2'].hide()
        self.checkresultwin_interface['c3'].hide()
        self.checkresultwin_interface['c4'].hide()
        
        self.checkresultwin_interface['ic1'].hide()
        self.checkresultwin_interface['ic2'].hide()
        self.checkresultwin_interface['ic3'].hide()
        self.checkresultwin_interface['ic4'].hide()

                
        answer = self.current_test[self.current_test_pos][0].answer
        user_answer = self.current_test[self.current_test_pos][1]
        
        if user_answer == answer:
            correct = "c%d"%answer
            
            self.checkresultwin_interface[correct].show()
        else:
            correct = "c%d"%answer
            incorrect = "ic%d"%user_answer
            
            self.checkresultwin_interface[correct].show()
            if user_answer != 0:    # if user did not skip the question
                self.checkresultwin_interface[incorrect].show()

        
        # This here is a special case, when there is only one question
        # in the database, we'll want to disable both next and back 
        # buttons. By default when the introspect
        if self.current_test_max == 1:
            self.checkresultwin_next.set_sensitive(False)
            
        self._checkresultwin_status_info_update(answer=answer, user_answer=user_answer)
        
    
    def _checkresultwin_next(self, widget, data=None):
        self.current_test_pos = self.current_test_pos +1
        
        if (self.current_test_pos +1) == self.current_test_max:
            self.checkresultwin_next.set_sensitive(False)
                
        if not self.checkresultwin_back.get_sensitive():
            self.checkresultwin_back.set_sensitive(True)
        
        self._checkresultwin_update()
        
        
    def _checkresultwin_back(self, widget, data=None):
        self.current_test_pos = self.current_test_pos -1
        
        if self.current_test_pos == 0:
            self.checkresultwin_back.set_sensitive(False)
        
        if not self.checkresultwin_next.get_sensitive():
            self.checkresultwin_next.set_sensitive(True)
        
        self._checkresultwin_update()

    # this methods updates the label at the bottom of result window to show whether
    # the question was skipped, answered correctly or answered incorrectly.
    def _checkresultwin_status_info_update(self, answer, user_answer):

        
        if user_answer == 0:
            self.checkresultwin_interface['status_info'].set_markup(
                "<b>Result: <span font_family='monospace' font='12' color='orange'>Skipped</span></b>")
        elif user_answer == answer:
            self.checkresultwin_interface['status_info'].set_markup(
                "<b>Result: <span font_family='monospace' font='12' color='green'>Correct</span></b>")
        else:
            self.checkresultwin_interface['status_info'].set_markup(
                "<b>Result: <span font_family='monospace' font='12' color='red'>Incorrect</span></b>")
        
        
    # hide the testwindow, cleanup stuff for the next test and go back to 
    # main window.

    def _stop_test(self, data=None):
        
        self.testwin.hide()
        self._cleanup()
        
        self.mainwin.show_all()
        
    
    # _new_test() is the starting point of the test. 
    # It calls _generate_test() to obtain a list of randomly selected 
    # parser.question objects from database, the number of objects being the 
    # number specified by user(25, 50, 100) or if the database doesn't have 
    # sufficient questions, then the maximum available questions.
    # It also sets up the first page of the test and leaves the rest of the
    # test to button widgets in testwin.

    
    def _new_test(self, length): # selection is the selected database
        
        # first we need to find the database that the user selected
        for db in self.database:
            if self.selection == db[0]: # the name of database 
                data = db[1]            # contents of the database
                
        self.current_test = self._generate_test(data, length) 
        
        if len(self.current_test) == 0:
            self._msg_db_empty_show(self.selection)
            del self.selection
            del self.current_test
            return None
            
        self.current_test_pos = 0           # this will be the current position 
        self.current_test_max = len(self.current_test) # max questions

               
        wait_timeleft = 5
        
        self.pretestwin.show_all()
        
        # warning: A little magic code ahead
        # the statement below forcefully redraws any widget pending to be 
        # redrawn, like when contents of a label are changed. The reason for 
        # doing this here is because without this, the label won't show, since
        # gtk would wait for us to finish process in the while loop below and
        # won't redraw till then, but i still haven't mastered gtk and still 
        # don't know gtk/gobject system that well, so feel free to correct me 
        # by mailing me
        
        self.pretestwin_label.set_markup(
             "<span font='25'>Your test will begin in <b>-</b> Seconds</span>")
        
        
        while gtk.events_pending():
                gtk.main_iteration(True)
        
        while wait_timeleft >= 0:
            
            self.pretestwin_label.set_markup(
            "<span font='25'>Your test will begin in <b>%d</b> Seconds</span>"%
                    wait_timeleft)
                    
            time.sleep(1)
                    
            wait_timeleft = wait_timeleft -1
            
            while gtk.events_pending():             # look at the comment above
                gtk.main_iteration(True)
                
        self.testwin.set_title(self.selection)
        
        self._testwin_update()
        
        self.pretestwin.hide()

        self.testwin_back.set_sensitive(False)

        # Show the testwindow
        self.testwin.show_all()

        # Start the timer
        self.timer.start(self.current_test_max * self.SECONDS_PER_QUESTION)

        # UI.test_is_active is an attribute that tells us if there's currently
        # an ongoing test i.e. the user is actively answering questions right 
        # now. This is used by the timer to check if time ran out while there
        # was an ongoing test.

        self.test_is_active = True
        
        
        
    
    def _msg_db_empty_ok_clicked(self, widget, event=None):
    
        self.msg_db_empty.hide()
        self.mainwin.show_all()
    
        return True

    def _msg_db_empty_show(self, database):
        message = "\
<span font_family='monospace' size='3'>The \"%s\" Database is Empty.</span>"%(
                                                                       database)

        self.msg_db_empty_data.set_markup(message)
        
        self.msg_db_empty.show_all()
    
    def _resultwin_exit(self, widget, event=None):
    
        self._cleanup()
        self.resultwin.hide()
        self.mainwin.show_all()

        return True
        
    def _cleanup(self):
        
        # highlight the invisible button, so that when next test starts, the 
        # last clicked button doesn't stay highlighted.
        
        self._testwin_disable_handlers()
        
        self.testwin_interface['btn0'].emit("clicked")  
        
        self._testwin_enable_handlers()

        # enable radiobuttons if they were previously disabled

        self._testwin_enable_radiobuttons()

        # enable back and next buttons if they were previously disabled

        self.checkresultwin_next.set_sensitive(True)
        self.checkresultwin_back.set_sensitive(True)
        
        # clear up the list that held the parser.question objects along with 
        # user response.
        
        for x in self.current_test:
            for y in x:
                del y
            del x
        del self.current_test
        
        del self.current_test_pos
        
        del self.current_test_max
        
        del self.selection
        
            
        
    def _result(self):

        # The test has concluded.
        self.test_is_active = False 

        self.timer.stop()

        self.testwin_interface['timer'].set_label("Time Left: --:--")

    
        result_max = self.current_test_max
        
        result_attempt = 0
        
        for question in self.current_test:
            if question[1] != 0:
                result_attempt = result_attempt +1
        
        result_correct = 0
        
        for question in self.current_test:
            answer = question[0].answer
            user_answer = question[1]
            
            if answer == user_answer:
                result_correct = result_correct +1
                
        
        result_incorrect = result_attempt - result_correct
        
        text = "<span font='13' font_family='monospace'><b>"
        text2 = "Your Score                   :%d/%d\n"%(result_correct, result_max)
        text3 = "-"*33+"\n"
        text4 = "\nTotal                        :%d\n"%(result_max)
        text5 = "\nAttempted                    :%d\n"%(result_attempt)
        text6 = "\nCorrect                      :%d\n"%(result_correct)
        text7 = "\nIncorrect                    :%d"%(result_incorrect)
        text8 = "</b></span>"
        
        result = text+text2+text3+text4+text5+text6+text7+text8
        
        self.resultwin_text.set_markup(result)
        
        self.resultwin.show_all()


    def _remove_thumbsdb(self, contents):

        # iterate through the contents of the contents and check
        # if any of the contents is 'thumbs.db', if found, remove
        # it from the list
        for index in range(len(contents)):
            if contents[index-1] == 'thumbs.db' or contents[index-1] == 'Thumbs.db':
                contents.pop(index)

    def _convert_seconds_to_mmss(self, s):
        "_convert_seconds_to_mmss(s) -> returns a string in the format of 'hh:mm:ss'"

        # converts seconds into it's equivalent hours minutes and time
        # format. The alogrithm itself is really simple. Most of the
        # code below format's the return string.

        minutes = s/60
        seconds = s%60

        hours = minutes/60

        if hours != 0:
            minutes = minutes%60
            if minutes < 10:
                if seconds <10:
                    return "%d:0%d:0%d"%(hours,minutes,seconds)
                else:
                    return "%d:0%d:%d"%(hours,minutes,seconds)
            else:
                if seconds <10:
                    return "%d:%d:0%d"%(hours,minutes,seconds)
                else:
                    return "%d:%d:%d"%(hours,minutes,seconds)
        else:
            if minutes < 10:
                if seconds <10:
                    return "0%d:0%d"%(minutes,seconds)
                else:
                    return "0%d:%d"%(minutes,seconds)
            else:
                if seconds <10:
                    return "%d:0%d"%(minutes,seconds)
                else:
                    return "%d:%d"%(minutes,seconds)

        
    
    ### Public Interface(s) ###

    def timer_tick(self):
        "timer_tick() -> None. This is the timeout that will\
be called by gobject.timeout_add() to facilitate timer functionality"

    
        time_left = self.timer.get_time()

        if time_left == 0:
            if self.test_is_active == True:
                # time ran out

                timer = self.testwin_interface['timer']
                timer.set_label("<span font='3'Time Left: --:--</span>")

                self._testwin_disable_radiobuttons()

                self.test_is_active = False
                self.timeoutwin.show_all()
            else:
                # there's no active test
                return True 

        else:
            mmss_left = self._convert_seconds_to_mmss(time_left)
            self.testwin_interface['timer'].set_label(
                                "<span font='9'> Time Left: %s</span>"%mmss_left)

        return True

    
    def set_database(self, database):
        "set_database(self, database) -> None"
    
        self.database = database
        
        for data in self.database:
            self.selectionwin_data.append([data[0]])

    def set_timer(self, timerobj):
        """set_timer(timerobj) -> Nothing.Setup's the timer that'll be used.
set_timer() expects the function to have a start(), stop() and get_time()
method. If your timer doesn't have these, you'll have to write wrapper code
for it yourself. start() must only take seconds as argument and get_time()
must return seconds left or 0 if timer ran out or was explictly stopped via
stop()"""
    
    # Please note that the UI obj does not check if timer
    # object provided has the aforementioned methods. It
    # is left upto the programmer to take care of this.
        self.timer = timerobj

    def start(self):
        self.mainwin.show_all()
        
    
    ### End of UI ###
        
        
        
def remove_extension(file, extension):
    "remove_extension(f, ext) -> str\nremoves ext from f and returns it"
    return file.replace(extension, '')
    

        
def database_init(path):
    #  database_init(path)-> list
    #  returns a list of databases along with their content in the form of 
    #  [('NameOfDatabase',[dataobjects])]
    #  which is basically a tuple containing the database name and a list 
    #  containing parser.question objects 
    
    database = []
    
    files = os.listdir(path)
    
    for f in files:
        x = parser.readfile(os.path.join(path,f), '##db##')
        
        # If there was some error is finding/opening a file
        # or if the file was not a db file
        if x == -1:
            continue
         
        data = (remove_extension(f, '.txt'), parser.parse(x))
        database.append(data)
        
    return database
        
### Main() Function ###

def main():
    databasepath = "database"
    database = database_init(databasepath)

    timer = new_timer() # create a new timer object
    
    interface = UI()   # Initialize Graphical User Interface
    
    interface.set_database(database)   # setup database

    interface.set_timer(timer)  # setup timer
    
    interface.start()

    # setup a callback which will be repeatedly called
    # during the execution of the program with an interval
    # of 500 ms
    gobject.timeout_add(500, interface.timer_tick)
    
    gtk.main()
   
    return 0
    

if __name__ == "__main__":
    sys.exit(main())
    
    
  
