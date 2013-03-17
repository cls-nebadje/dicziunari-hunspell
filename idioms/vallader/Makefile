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

# http://kb.mozillazine.org/Dictionaries

TOOLSDIR=../../tools

RM=rm -rf
SHELL=bash
PDFWL=$(TOOLSDIR)/pdf2wl.py
LANG=rm-Vallader

# Sources
AFFIX=$(LANG).aff

# pdf wordlist dirs
RESDIR=resources
PDFWORDLISTDIRS=$(RESDIR)/engadiner-post

# Outputs
TARGET=$(LANG).dic
SEEDWORDLIST=$(LANG).wl
PDFWORDLISTS=$(addsuffix /$(LANG).wl,$(PDFWORDLISTDIRS))
WORDLISTS= $(SEEDWORDLIST) $(PDFWORDLISTS)
DICTDB=$(LANG).db

# Seed dict
SEEDLANG=$(LANG)-seed
SEEDDICT=$(SEEDLANG).dic
SEEDAFF=$(SEEDLANG).aff

$(TARGET): $(WORDLISTS) $(AFFIX)
	cat $(WORDLISTS) > tmp.wl
	munch tmp.wl $(AFFIX) > $@
	rm tmp.wl

$(SEEDAFF): $(AFFIX)
	cp $< $@

$(SEEDDICT): $(SEEDWORDLIST) $(SEEDAFF)
	munch $^ > $@

$(SEEDWORDLIST): $(DICTDB)
	./genwordlists.py

$(PDFWORDLISTS): $(SEEDDICT)
	$(PDFWL) $(SEEDLANG) $(dir $@)pdf $(dir $@)$(LANG).wl
	

$(DICTDB):
	./gendatabase.sh $@


all: $(TARGET)

clean:
	$(RM) $(TARGET) $(WORDLISTS) $(SEEDDICT) $(SEEDAFF)

mr-proper: clean
	$(RM) $(DICTDB)

new: clean all

wordlists: clean $(WORDLISTS)

install: $(TARGET)
	sudo cp $(AFFIX) $(TARGET) /usr/lib/thunderbird/dictionaries/
	
charprobab: $(WORDLISTS)
	./charprob.py
