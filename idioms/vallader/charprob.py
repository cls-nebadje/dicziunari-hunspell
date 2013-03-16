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

#
# Character probability for 'TRY' statement in affix files
#

import re, string

f = open("rm-Vallader.wl")
data = f.read().decode("utf-8")
f.close()

# erase all punctuation, numbers, special characters
others = u" \n\r\u2019\u2020"
RX_PUNCT = re.compile('[%s]' % re.escape(string.punctuation+string.digits+others),
                      re.MULTILINE)

data = RX_PUNCT.sub('', data)

chars = {}
for c in data:
    chars[c] = chars.get(c, 0) + 1

chars = sorted(chars.items(), key=lambda (k,v): (v,k), reverse=True)

print "".join([k for k, _ in chars])
