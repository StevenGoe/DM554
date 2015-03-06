import textwrap
import re
import subprocess
import os
import errno

# Version: 0.1

class LatexDocument:
    def __init__(self, filename):
        self.filename = filename
        self.ext = "tex"
        self.preambleTemplate = self.prepareLatex(r"""
            \documentclass[12pt, a4paper]{article}
            
            % Font & text
            \usepackage{times}
            \usepackage[utf8]{inputenc} 
            \setlength{\parindent}{0in}
            \usepackage{hyperref}
            \hypersetup{%
                pdfborder = {0 0 0}
            }
            \usepackage{caption}
            \usepackage{subcaption}
            \usepackage{float}
            
            % Math
            \usepackage{amsmath}
            \usepackage{amssymb}
        """)
        self.documentTemplate = self.prepareLatex(r"""
            \begin{document}
            %{lines}%
            \end{document}
        """)
        self.lines = []

    def line(self, s = ""):
        self.lines.append(s)

    def skip(self, size = "med"):
        self.line()
        if size == "med" or size == "medium":
            self.line(r"\medskip")
        elif size == "big" or size == "large":
            self.line(r"\bigskip")
        elif size == "small":
            self.line(r"\smallskip")
        self.line()

    def linebreak(self):
        self.line()
        self.line()

    def pagebreak(self):
        self.line(r"\newpage")

    def render(self):
        preambleDict = {}
        documentDict = {
            'lines': '\n'.join(self.lines)
        }
        return "%s\n%s" %  (self.preambleTemplate.format(**preambleDict), 
                            self.documentTemplate.format(**documentDict))

    def to_file(self):
        r = self.render()
        filename = "%s.%s" % (self.filename, self.ext)
        folder = self.filename
        self.make_sure_path_exists(folder)
        path = os.path.join(folder, filename)
        with open(path,'w') as f:
            f.write(r)
        return (folder, filename)

    def compile(self):
        (folder, filename) = self.to_file()
        path = os.path.join(folder, filename)
        origWD = os.getcwd()
        os.chdir(folder)
        subprocess.call(["pdflatex", filename])
        os.chdir(origWD)

    def prepareLatex(self, latex):
        return self.prepareLatexFormat(textwrap.dedent(latex))

    def prepareLatexFormat(self, latex):
        escapeCurly = latex.replace("{", "{{").replace("}", "}}")
        return self.replaceAll(escapeCurly, {
            "%{{": "{",
            "}}%": "}"
        })

    def replaceAll(self, s, d):
        pattern = re.compile('|'.join(d.keys()))
        return pattern.sub(lambda x: d[x.group()], s)

    def make_sure_path_exists(self, path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

class LatexDocumentVoid(LatexDocument):
    def __init__(self, *args):
        pass
    def line(self, *args):
        pass
    def render(self, *args):
        return ""

vdoc = LatexDocumentVoid()
