#!/usr/bin/python

import commands, tempfile, re, sys, os

urls = ["http://www.sent-online.ch/organisaziun/publicaziuns_ufficialas/protocols/cussegl/archiv-protocols_r_c.html",
        "http://www.sent-online.ch/organisaziun/publicaziuns_ufficialas/protocols/cussegl/2011/index.html",
        "http://www.sent-online.ch/organisaziun/publicaziuns_ufficialas/protocols/cussegl/2012/index.html",
        "http://www.sent-online.ch/organisaziun/publicaziuns_ufficialas/protocols/cussegl/2013/index.html",
        "http://www.sent-online.ch/organisaziun/publicaziuns_ufficialas/mas_chalchs/index.html",
        ]

pdfUrls = []

RX_PDF_URL = re.compile(r'href="(http://\S+?.pdf)"', re.MULTILINE)
RX_PDF_URL_REL = re.compile(r'href="(?!http:)(\S+?.pdf)"', re.MULTILINE)

def getPdfUrlsFromUrl(url):
    base = os.path.dirname(url)
    t = tempfile.NamedTemporaryFile()
    s, o = commands.getstatusoutput('wget --output-document=%s "%s"' % (t.name, url))
    if s == 0:
        html = t.read().decode("utf-8")
        u = RX_PDF_URL.findall(html)
        u += ["%s/%s" % (base, p) for p in RX_PDF_URL_REL.findall(html)]
        return u
    else:
        print >> sys.stderr, "Failed to load page from %s: %s (%i)" % (url, o, s)
    return []

SHELLSCRIPT="dl-sent-online-pdfs.sh"
sh = open(SHELLSCRIPT, "w")

lines = ["#!/bin/bash",
         "mkdir -p pdf",
         "cd pdf"]

for url in urls:
    for pdf in getPdfUrlsFromUrl(url):
        lines.append('wget "%s"' % pdf)

lines.append("for f in `ls *.pdf.*`; do mv $f ${f}.pdf; done")
lines.append("cd ..")

sh.write("\n".join(lines) + "\n")
sh.close()

commands.getstatusoutput("chmod +x %s" % SHELLSCRIPT)

