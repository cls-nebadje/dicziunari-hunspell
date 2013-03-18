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
import sys, sqlite3, re, string

def main():
    
    if len(sys.argv) < 3:
        print >> sys.stderr, "Too few arguments."
        return 1
    
    dbPath = sys.argv[1]
    wlPath = sys.argv[2]
    
    # TODO get DB file name and output file name from command line arguments...
    db = sqlite3.connect(dbPath)
    cur = db.cursor()
    sql = "SELECT pled FROM dicziunari GROUP BY pled"
    cur.execute(sql)
    
    # We use a set to get unique entries
    words = set()
    for row in cur.fetchall():
        wl_dicz_proc_row(words, row)
    
    wl = open(wlPath, "w")
    for w in words:
        w = u"%s\n" % w
        wl.write(w.encode("utf-8"))
    wl.close()
    
    return 0

def wl_dicz_proc_masc_fem(words, stem, femfin):
    words.add(stem)
    # Experimental masc plural:
    if stem[-1] != "s":
        words.add(stem + "s")
    # Compute feminin
    if femfin in ['a', 'ta', 'za', 'la']:
        fem = stem + femfin
        words.add(fem)
        words.add(fem + "s")
    else:
        f = femfin[0]
        p = stem.rfind(f)
        fem = stem[:p] + femfin
        words.add(fem)
        # Experimental fem plural:
        if stem[-1] != "s":
            words.add(fem + "s")               

    
# Finds masc/fem pairs
RX_MF     = re.compile(r'(\S+?),\s+-(\S+?)(?=\s|$)')
RX_MF_DEL = re.compile(r'(\S+?,\s+-\S+?)(?=\s|$)')


def wl_dicz_proc_row_entry(entry):
    words = set()
    
    # Remove german cross references
    if entry.startswith("cf. "):
        return words
    
    # Find all masc/fem pairs
    m = RX_MF.findall(entry)
    if len(m):
#        print "a:", entry
        for stem, femfin in m:
            wl_dicz_proc_masc_fem(words, stem, femfin)
        # As we extracted the words we have to delete them from the entry
        entry = RX_MF_DEL.sub(' ', entry)
    
    # Add remaining words
    entry = entry.strip()
    if len(entry) > 0:
        for w in entry.split(" "):
            words.add(w)
 
    # Split on white space
    return words


# Regex to erase punctuation
RX_PUNCT = re.compile('[%s]' % re.escape(string.punctuation + "/()"))

def wl_dicz_proc_row(words, row):
    if row[0] is not None:
        for w in wl_dicz_proc_row_entry(row[0].strip()):
            nw = RX_PUNCT.sub('', w).strip()
            if len(nw) > 0:
                words.add(nw)

if __name__ == "__main__":
    sys.exit(main())
