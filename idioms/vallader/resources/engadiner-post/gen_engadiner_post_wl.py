#!/usr/bin/python

import sys, os, re, tempfile, commands

def main():

    N = 50  # Number of pdfs to analyze
    
    words = set()
    for p in os.listdir("pdf/"):
        be = os.path.splitext(p)
        if len(be) == 2 and be[1].lower() == ".pdf":
            words = words.union(processPdf("pdf/%s" % p))
        N -= 1
        if N <= 0:
            break
            
    # TODO: Remove german words by applying a german hunspell ditionary
    
    wl = open("rm-Vallader-engadiner-post.wl", "w")
    wl.writelines([("%s\n"%w).encode("utf-8") for w in words])
    wl.close()
    
    return 0
    
RX_WORDCOUNT = re.compile(r'\w+')

def processPdf(path):
    
    words = set()

    txtFile = tempfile.NamedTemporaryFile()
    s, o = commands.getstatusoutput("pdftotext %s %s" % (path, txtFile.name))
    if s != 0:
        print sys.stderr >> "Failed to convert pdf to text: %s (%i)" % (o, s)
        return words
    lines = txtFile.read().decode("utf-8")
    txtFile.close()
    del txtFile
    
    lines = [l.strip() for l in lines.splitlines()]
        
    p = []
    for line in lines:
        if len(line) == 0:
            # Only add substantial amount of text
            p = " ".join(p)
            pWords = RX_WORDCOUNT.findall(p)
            N = len(pWords)
            if N > 100:  # only consider substantial paragraphs
                if isVallader(p, N):
                    processWords(words, pWords)
            p = []
            continue
    
        p.append(line)

    return words

def processWords(words, newWords):
    """ """
    for w in newWords:
        # Clean up trash
        words.add(w)

def isVallader(p, nWords):
    f = tempfile.NamedTemporaryFile()
    f.write(p.encode("utf-8"))
    f.flush()
    cmd = "hunspell -l -i utf-8 -d ../../rm-Vallader %s" % f.name
    s, o = commands.getstatusoutput(cmd)
    if s != 0:
        return False
    o = o.decode("utf-8")
    nMisspelled = len(o.splitlines())
    ratio = float(nWords - nMisspelled) / float(nWords)
    
    res = ratio > 0.8
    if res:
        print ratio
    return res

if __name__ == "__main__":
    sys.exit(main())
