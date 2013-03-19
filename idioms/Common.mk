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
GLOBALRESDIR=../../resources
RESDIR=resources
BLACKLISTDIR=$(RESDIR)/blacklists

# Tools
RM=rm -rf
SHELL=bash
SQLITEWL=$(TOOLSDIR)/sqlite2wl.py
PDFWL=$(TOOLSDIR)/pdf2wl.py
MAKEDB=./makedb.sh
CHARPROB=$(TOOLSDIR)/charprob.py
BL=$(TOOLSDIR)/blacklist.py

# Sources
AFFIX=$(LANG).aff
INSTALLRDFTEMPLATE=$(TEMPLATEDIR)/install.rdf
BLACKLISTS=$(shell ls $(BLACKLISTDIR)/*.wl)
ICON=$(GLOBALRESDIR)/icon.png

# Outputs
TARGET=$(LANG).dic
SEEDWORDLIST=$(LANG).wl
PDFWORDLISTS=$(addsuffix /$(LANG).wl,$(PDFWORDLISTDIRS))
WORDLISTS= $(SEEDWORDLIST) $(PDFWORDLISTS)
DICTDB=$(LANG).db
INSTALLRDF=install.rdf
XPI=$(LANG).xpi

# Seed dict
SEEDLANG=$(LANG)-seed
SEEDDICT=$(SEEDLANG).dic
SEEDAFF=$(SEEDLANG).aff

CP=$(shell $(CHARPROB) $(WORDLISTS))

$(XPI): $(TARGET) $(AFFIX) $(INSTALLRDF) $(ICON)
	rm -rf .tmp
	mkdir -p .tmp/dictionaries
	cp $(INSTALLRDF) .tmp/
	cp $(ICON) .tmp/
	cp $(TARGET) $(AFFIX) .tmp/dictionaries/
	cd .tmp; zip ../$@ -r *; cd ..
	rm -rf .tmp

$(TARGET): $(WORDLISTS) $(AFFIX) $(BLACKLISTS)
	# Add char probability to affix file
	# echo "$(CP)"
	cat $(WORDLISTS) > tmp.wl
	$(BL) tmp.wl tmp.wl $(BLACKLISTS)
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

# XPI package ID
ID=$(LANG)@dictionaries.addons.mozilla.org

$(INSTALLRDF): $(INSTALLRDFTEMPLATE)
	sed -e "s/__ID__/$(ID)/g" \
	    -e "s/__VERSION__/$(VERSION)/g" \
	    -e "s/__NAME_EN__/$(NAME_EN)/g" \
	    -e "s/__DESC_EN__/$(DESC_EN)/g" \
	    -e "s/__AUTH_EN__/$(AUTH_EN)/g" \
	    -e "s/__NAME_DE__/$(NAME_DE)/g" \
	    -e "s/__DESC_DE__/$(DESC_DE)/g" \
	    -e "s/__AUTH_DE__/$(AUTH_DE)/g" \
	    $< > $@


all: $(XPI)

clean:
	$(RM) $(TARGET) $(WORDLISTS) $(SEEDDICT) $(SEEDAFF) $(INSTALLRDF) $(XPI)

mr-proper: clean
	$(RM) $(DICTDB)

new: clean all

wordlists: clean $(WORDLISTS)

# sudo cp $(AFFIX) $(TARGET) /usr/lib/thunderbird/dictionaries/
install: $(XPI)
	for d in `find ~/.thunderbird/ -name "*.default"`; do \
		mkdir -p $$d/extensions/$(ID)/;                   \
		unzip -o $(XPI) -d $$d/extensions/$(ID)/ ;           \
	done
	for d in `find ~/.mozilla/firefox/ -name "*.default"`; do \
		mkdir -p $$d/extensions/$(ID)/;                       \
		unzip -o $(XPI) -d $$d/extensions/$(ID)/ ;               \
	done

# sudo rm /usr/lib/thunderbird/dictionaries/$(LANG)*
uninstall:
	for d in `find ~/.thunderbird/ -name "*.default"`; do \
		rm -rf $$d/extensions/$(ID);                      \
	done
	for d in `find ~/.mozilla/firefox/ -name "*.default"`; do \
		rm -rf $$d/extensions/$(ID);                          \
	done
	
charprobab: $(WORDLISTS)
	$(CHARPROB) $^
