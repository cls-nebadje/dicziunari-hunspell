#!/usr/bin/python
# coding=utf-8
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

""" Program to expand the dictionary of a language defined by a so called
"seed dictionary" by extracting paragraphs from pdfs an guessing the
language of each paragraph and add the words of those paragraphs to the
language's dictionary.
"""

import sys, os, re, tempfile, commands

# Minimum size of a paragraph to be considered at all.
MIN_SIZE_PARAGRAPH = 1000

# Minimum ratio of misspelled words compared to correctly spelled words in
# order to consider the paragraph being of the given language 
MIN_RATIO_PARAGRAPH_ACCEPT = 0.8

def main():

    if len(sys.argv) < 4:
        print >> sys.stderr, "Too few arguments. Usage: %s <seed-dict> <pdf-dir> <output-file>" % sys.argv[0]
        return 1
    seedDict    = sys.argv[1]
    pdfDir      = sys.argv[2]
    outFilePath = sys.argv[3]

    N = 1000  # Number of pdfs to analyze
    i = 0
    
    words = set()
    
    files = os.listdir(pdfDir)
    N = min(N, len(files))
    for p in files:
        i += 1
        if i > N:
            break
        
        be = os.path.splitext(p)
        if len(be) == 2 and be[1].lower() == ".pdf":
            print "Processing [%3i/%3i]: %s" % (i, N, p)
            newWords = processPdf(seedDict, os.path.join(pdfDir, p))
            words = words.union(newWords)
            
    # TODO: Remove german words by applying a german hunspell ditionary
    
    wl = open(outFilePath, "w")
    wl.writelines([("%s\n"%w).encode("utf-8") for w in words])
    wl.close()
    
    return 0

# Regex to split words but keeping apostrophed stuff intact
RX_WORD_SPLIT = re.compile(r'\w+(?:\'\w+)*', re.UNICODE)

def processPdf(seedDict, path):
    """
    """
    words = set()
    
    txtFile = tempfile.NamedTemporaryFile()
    s, o = commands.getstatusoutput("pdftotext %s %s" % (path, txtFile.name))
    if s != 0:
        print >> sys.stderr, "Failed to convert pdf to text: %s (%i)" % (o, s)
        return words
    try:
        lines = txtFile.read().decode("utf-8")
    except Exception as e:
        print >> sys.stderr, "Failed to read/decode %s: %s" % (path, str(e))
        return words
    txtFile.close()
    del txtFile
    
    lines = [l.strip() for l in lines.splitlines()]
        
    p = []
    for line in lines:
        if len(line) == 0:
            p = " ".join(p)
            if len(p) > MIN_SIZE_PARAGRAPH:   # only consider substantial paragraphs
                p = preprocessParagraph(p)
                pWords = RX_WORD_SPLIT.findall(p)
                N = len(pWords)
                if isIdiom(seedDict, p, N):
                    processWords(words, pWords)
            p = []
            continue
    
        p.append(line)

#    print words
    
    return words

# Detect words composed solely of digits (years, telephone numbers, ...)
RX_NUMBER = re.compile(r'^[0-9]+$', re.UNICODE)

def processWords(words, newWords):
    """ Remove trash and add words to set. """
    for w in newWords:
        # Remove numbers
        if RX_NUMBER.match(w) != None:
            continue
        words.add(w)

# Pdf to text produces the \u2019 apostrophe but we use "'" -> replace
RX_REPLACE_PDF_APOSTROPHE = re.compile(r'[%s]'%re.escape(u"\u2019"), re.UNICODE)

def preprocessParagraph(p):
    """ Apply some processing before splitting the paragraph into words.
    Currently it just converts the pdf/engadiner-post typical apostrophe into
    an apostrophe used within our hunspell dictionaries.
    
    @todo: Handle hyphenation within the paragraph. Examples I found in the
           resulting wordlist: ["l'instru"]
    """
    p = RX_REPLACE_PDF_APOSTROPHE.sub("'", p)
    return p
    
def isIdiom(seedDict, p, nWords, thresh=MIN_RATIO_PARAGRAPH_ACCEPT):
    """ Checks if the given paragraph is of the idiom/language defined by the
    seed dictionary.
    
    @param seedDict: Path to a hunspell dictionary (consisting of .dic and .aff
                     files). This seed dictionary determines the idiom/language
                     to be detected.
    @param p:        Paragraph to be checked
    @param nWords:   Number of words within the paragraph
    @param thresh:   Threshold at which a paragraph is considered to be of the
                     language determined by seedDict. Must be in the range
                     0.0 .. 1.0, whereas 0 means that no words are required to
                     be correct, 1.0 that all words must be covered by the
                     seedDict. 
    """
    
    if nWords <= 0:
        return False
    
    f = tempfile.NamedTemporaryFile()
    f.write(p.encode("utf-8"))
    f.flush()
    cmd = "hunspell -l -i utf-8 -d %s %s" % (seedDict, f.name)
    s, o = commands.getstatusoutput(cmd)
    if s != 0:
        return False
    try:
        o = o.decode("utf-8")
    except Exception as e:
        print >> sys.stderr, "Failed to decode hunspell output: %s" % (str(e))
        return False
    
    nMisspelled = len(o.splitlines())
    ratio = float(nWords - nMisspelled) / float(nWords)
    
    res = ratio > thresh
    if res:
        print "%3i%% - %i words" % (int(ratio*100), nWords)
    return res

if __name__ == "__main__":
    sys.exit(main())
