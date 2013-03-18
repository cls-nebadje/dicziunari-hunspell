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

# Directories
TOOLSDIR=../../tools
TEMPLATEDIR=../../templates
RESDIR=resources

# Tools
RM=rm -rf
SHELL=bash
SQLITEWL=$(TOOLSDIR)/sqlite2wl.py
PDFWL=$(TOOLSDIR)/pdf2wl.py
MAKEDB=makedb.sh
CHARPROB=$(TOOLSDIR)/charprob.py

# Sources
AFFIX=$(LANG).aff
INSTALLRDFTEMPLATE=$(TEMPLATEDIR)/install.rdf

# Outputs
TARGET=$(LANG).dic
SEEDWORDLIST=$(LANG).wl
PDFWORDLISTS=$(addsuffix /$(LANG).wl,$(PDFWORDLISTDIRS))
WORDLISTS= $(SEEDWORDLIST) $(PDFWORDLISTS)
DICTDB=$(LANG).db
INSTALLRDF=install.rdf

# Seed dict
SEEDLANG=$(LANG)-seed
SEEDDICT=$(SEEDLANG).dic
SEEDAFF=$(SEEDLANG).aff

CP=$(shell $(CHARPROB) $(WORDLISTS))

$(TARGET): $(WORDLISTS) $(AFFIX)
	# Add char probability to affix file
	# echo "$(CP)"
	cat $(WORDLISTS) > tmp.wl
	munch tmp.wl $(AFFIX) > $@
	rm tmp.wl

$(SEEDAFF): $(AFFIX)
	cp $< $@

$(SEEDDICT): $(SEEDWORDLIST) $(SEEDAFF)
	munch $^ > $@

$(SEEDWORDLIST): $(DICTDB)
	$(SQLITEWL) $< $@

$(PDFWORDLISTS): $(SEEDDICT)
	$(PDFWL) $(SEEDLANG) $(dir $@)pdf $(dir $@)$(LANG).wl

$(DICTDB):
	$(MAKEDB) $@

$(INSTALLRDF): $(INSTALLRDFTEMPLATE)
	sed -e "s/__LANG__/$(LANG)/g" \
	    -e "s/__VERSION__/$(VERSION)/g" \
	    -e "s/__NAME_EN__/$(NAME_EN)/g" \
	    -e "s/__DESC_EN__/$(DESC_EN)/g" \
	    -e "s/__AUTH_EN__/$(AUTH_EN)/g" \
	    -e "s/__NAME_DE__/$(NAME_DE)/g" \
	    -e "s/__DESC_DE__/$(DESC_DE)/g" \
	    -e "s/__AUTH_DE__/$(AUTH_DE)/g" \
	    $< > $@


all: $(TARGET)

clean:
	$(RM) $(TARGET) $(WORDLISTS) $(SEEDDICT) $(SEEDAFF) $(INSTALLRDF)

mr-proper: clean
	$(RM) $(DICTDB)

new: clean all

wordlists: clean $(WORDLISTS)

install: $(TARGET)
	sudo cp $(AFFIX) $(TARGET) /usr/lib/thunderbird/dictionaries/
	
charprobab: $(WORDLISTS)
	$(CHARPROB) $^
