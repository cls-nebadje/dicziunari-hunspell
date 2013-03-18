#!/usr/bin/python
#
# Dicziunari-Hunspell -- Rhaeto-Romance hunspell dictionary generation
# 
# Copyright (C) 2012-2013 Uli Franke (cls) et al.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# IMPORTANT NOTICE: All software, content, intellectual property coming
# with this program (usually contained in files) can not be used in any
# way by the Lia Rumantscha (www.liarumantscha.ch/) without explicit
# permission, as they actively block software innovation targeting the
# Rhaeto-Romance language.
#

""" Blacklist filter a word list with black lists and output a new word list
"""
import sys, dzhs.wordlist as wordlist

def main():
    """ """
    if len(sys.argv) < 4:
        print >> sys.stderr, "Invalid argument count: Usage <out> <bl> <wl>"
        return 1
    outPath  = sys.argv[1]
    wlPath   = sys.argv[2]
    blPaths   = sys.argv[3:]
    
    wl = wordlist.load(wlPath)
    N = len(wl)
    
    for blPath in blPaths:
        bl = wordlist.load(blPath)
        wl = wl.difference(bl)

    B = N - len(wl)
    print "Blacklisted %i words." % (B)
            
    wordlist.store(outPath, wl)

    return 0
    
if __name__ == "__main__":
    sys.exit(main())

