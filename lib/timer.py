#                timer.py - Timer functionalities
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

import pygtk
import gtk
import gobject
from time import time

class timer(object):
    def __init__(self):

        self.timeleft = 0
        self.startime = 0
        self.last_return = 0
        self.last_recaliberation = 0
        self.duration = 0

        self.RECALIBERATE_PERIOD = 5

    def get_time(self):

        if self.timeleft == 0:
            return 0

        if ( time() - self.last_recaliberation) >= self.RECALIBERATE_PERIOD:
            self._recaliberate()

        if ( time() - self.last_return) < 1:
            return self.timeleft
        else:
            self.timeleft -= 1
            self.last_return = time()
            return self.timeleft

    def _recaliberate(self):
        current_time = time()

        self.timeleft = self.duration - int(current_time - self.starttime)

        self.last_recaliberation = current_time

    def start(self, seconds):

        self.last_recaliberation = time()

        self.starttime = time()

        self.duration = seconds
        self.timeleft = seconds



    def stop(self):

        self.timeleft = 0
        self.last_recaliberation = 0
        self.last_return = 0
        self.startime = 0
        self.duration = 0
