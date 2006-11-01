#!/usr/bin/env python
import os, re, string
from cStringIO import StringIO 
from optparse import OptionParser
from pygments import highlight
from pygments.lexers import JavascriptLexer
from pygments.formatters import HtmlFormatter

class DocHighlighter(object):

    def __init__(self, inputdirs, outputdir, ext, newext):

        def _mkdir(newdir):
            if os.path.isdir(newdir): pass
            elif os.path.isfile(newdir):
                raise OSError("a file with the same name as the desired " \
                              "dir, '%s', already exists." % newdir)
            else:
                head, tail = os.path.split(newdir)
                if head and not os.path.isdir(head): _mkdir(head)
                if tail: os.mkdir(newdir)

        def highlightString(src):
            return highlight(src, JavascriptLexer(), HtmlFormatter())

        def highlightFile(path, file):
            #print path + ", " + file
            f=open(os.path.join(path, file))
            fileStr=StringIO(f.read()).getvalue()
            f.close()
            print "highlighting " + file

            highlighted = highlightString(fileStr)

            out = open(os.path.join(self.outputdir, file + self.newext), "w")
            out.writelines(highlighted)
            out.close()

        def highlightDir(path):
            subdirs = []
            dircontent = ""
            for i in os.listdir(path):
                fullname = os.path.join(path, i)
                if os.path.isdir(fullname):
                    subdirs.append(fullname)
                elif i.lower().endswith(self.ext):
                    highlightFile(path, i)

            for i in subdirs:
                highlightDir(i)

        self.inputdirs = inputdirs
        self.outputdir = os.path.abspath(outputdir)
        _mkdir(self.outputdir)
        self.ext = ext
        self.newext = newext

        print "-------------------------------------------------------"

        for i in inputdirs: 
            highlightDir(os.path.abspath(i))


def main():
    optparser = OptionParser("usage: %prog [options] inputdir1 inputdir2 etc")
    optparser.set_defaults(outputdir="out", ext=".js", newext=".highlighted")
    optparser.add_option( "-o", "--outputdir",
                          action="store", dest="outputdir", type="string",
                          help="Directory to write the parser results" )
    optparser.add_option( "-e", "--extension",
                          action="store", dest="ext", type="string",
                          help="The extension for the files that should be parsed" )
    optparser.add_option( "-n", "--newextension",
                          action="store", dest="newext", type="string",
                          help="The extension to append to the output file" )
    (opts, inputdirs) = optparser.parse_args()
    if len(inputdirs) > 0:
        docparser = DocHighlighter( inputdirs, 
                            opts.outputdir, 
                            opts.ext,
                            opts.newext )
    else:
        optparser.error("Incorrect number of arguments")
           
if __name__ == '__main__':
    main()
