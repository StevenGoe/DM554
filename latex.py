import textwrap
import re
import subprocess
import os
import errno
import numpy as np

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

            % Gaussian Elimination
            \usepackage{gauss}

            % Gauss patch
            % http://tex.stackexchange.com/questions/146532/
            \usepackage{etoolbox}
            \makeatletter
            \patchcmd\g@matrix
            {\vbox\bgroup}
            {\vbox\bgroup\normalbaselines}
            {}{}
            \makeatother

            \newcommand{\BAR}{
              \hspace{-\arraycolsep}
              \strut\vrule
              \hspace{-\arraycolsep}
            }
        """)
        self.documentTemplate = self.prepareLatex(r"""
            \begin{document}
            %{lines}%
            \end{document}
        """)
        self.lines = []

    def subdoc(self):
        return LatexDocument("%s-sub" % self.filename)

    def line(self, s = ""):
        self.lines.append(s)

    def write(self, s = "", prefix = " ", postfix = " "):
        if len(self.lines) == 0:
            self.line()
        self.lines[-1] += (prefix + s + postfix)

    def from_subdoc(self, doc):
        for line in doc.lines:
            self.line(line)

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

    def matrix(self, A, typ="b", delim=None, rowops=None):
        m, n = A.shape
        self.line(r"\begin{gmatrix}[%s]" % typ)
        newline = r" \\ "

        for i in range(m):
            l = []
            for j in range(n):
                l.append(self.frac(A[i,j]))
                if j == delim:
                    l.append(r"\BAR")
            self.line(" & ".join(l) + (newline if i < m-1 else ""))

        if rowops:
            self.line(r"\rowops")
            for s in rowops:
                self.line(s)

        self.line(r"\end{gmatrix}")

    def frac(self, f):
        if "/" not in str(f):
            return str(f)
        else:
            sign = -1 if f < 0 else 1
            return r"%s\frac{%d}{%d}" % ("-" if sign == -1 else "", sign * f.numerator, f.denominator)

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
    def write(self, *args):
        pass
    def render(self, *args):
        return ""

vdoc = LatexDocumentVoid()
