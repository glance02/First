\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{csreport}[2026/05/13 Computer School course report class]

\LoadClass[UTF8,a4paper,zihao=-4]{ctexart}

\RequirePackage[
  a4paper,
  top=2cm,
  bottom=2cm,
  left=2cm,
  right=2cm,
  bindingoffset=0.5cm,
  headheight=14pt,
  headsep=0.35cm,
  footskip=1.75cm
]{geometry}
\RequirePackage{amsmath}
\RequirePackage{caption}
\RequirePackage{enumitem}
\RequirePackage{fancyhdr}
\RequirePackage{fontspec}
\RequirePackage{graphicx}
\RequirePackage{indentfirst}
\RequirePackage{setspace}
\RequirePackage{tocloft}

\IfFontExistsTF{Times New Roman}{\setmainfont{Times New Roman}}{}
\IfFontExistsTF{SimSun}{\newCJKfontfamily\songbold[FakeBold=2.5]{SimSun}}{\newcommand{\songbold}{\songti\bfseries}}

\setstretch{1.5}
\setlength{\parindent}{2em}
\setlength{\parskip}{0pt}
\setlist{nosep}
\pagestyle{empty}

\newcommand{\csreport@coursename}{课程名称}
\newcommand{\coursename}[1]{\renewcommand{\csreport@coursename}{#1}}

\fancypagestyle{csreportstyle}{
  \fancyhf{}
  \fancyhead[C]{\zihao{-5}\songti 《\csreport@coursename》课程报告}
  \fancyhead[R]{\zihao{-5}\songti 第\thepage 页}
  \renewcommand{\headrulewidth}{0.4pt}
  \renewcommand{\footrulewidth}{0pt}
}
\fancypagestyle{plain}{
  \fancyhf{}
  \fancyhead[C]{\zihao{-5}\songti 《\csreport@coursename》课程报告}
  \fancyhead[R]{\zihao{-5}\songti 第\thepage 页}
  \renewcommand{\headrulewidth}{0.4pt}
  \renewcommand{\footrulewidth}{0pt}
}

\newcommand{\reportbody}{%
  \clearpage
  \pagenumbering{arabic}%
  \pagestyle{csreportstyle}%
}

\ctexset{
  section = {
    format = \centering\zihao{-3}\heiti,
    name = {},
    number = \arabic{section},
    aftername = \quad,
    beforeskip = 1.5ex plus .2ex,
    afterskip = 1.5ex plus .2ex
  },
  subsection = {
    format = \zihao{4}\heiti,
    name = {},
    number = \thesection.\arabic{subsection},
    aftername = \quad,
    beforeskip = 1.2ex plus .2ex,
    afterskip = 1.0ex plus .2ex
  },
  subsubsection = {
    format = \zihao{-4}\songbold,
    name = {},
    number = \thesubsection.\arabic{subsubsection},
    aftername = \quad,
    beforeskip = 1.0ex plus .2ex,
    afterskip = 0.8ex plus .2ex
  }
}

\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{3}
\renewcommand{\contentsname}{目\quad\quad 录}
\renewcommand{\cfttoctitlefont}{\hfill\zihao{3}\heiti}
\renewcommand{\cftaftertoctitle}{\hfill}
\setlength{\cftbeforesecskip}{0.2em}

\renewcommand{\figurename}{图}
\renewcommand{\tablename}{表}
\renewcommand{\thefigure}{\thesection.\arabic{figure}}
\renewcommand{\thetable}{\thesection.\arabic{table}}
\renewcommand{\theequation}{\thesection.\arabic{equation}}
\@addtoreset{figure}{section}
\@addtoreset{table}{section}
\@addtoreset{equation}{section}
\captionsetup{font={small},labelsep=quad}
\captionsetup[table]{position=top}
\captionsetup[figure]{position=bottom}

\newenvironment{abstractcn}{%
  \clearpage
  \pagestyle{empty}%
  \begin{center}\zihao{3}\heiti 摘要\end{center}%
  \zihao{-4}\songti
}{\par}

\newenvironment{abstracten}{%
  \clearpage
  \pagestyle{empty}%
  \begin{center}\zihao{3}\bfseries ABSTRACT\end{center}%
  \zihao{-4}\rmfamily
}{\par}

\newcommand{\keywords}[1]{%
  \par\vspace{1em}\noindent{\heiti 关键词：}{#1}\par
}
\newcommand{\enkeywords}[1]{%
  \par\vspace{1em}\noindent{\bfseries Keywords: }#1\par
}

\renewenvironment{thebibliography}[1]{%
  \clearpage
  \section*{\zihao{4}\heiti 参考文献}%
  \addcontentsline{toc}{section}{参考文献}%
  \zihao{5}\songti
  \list{[\arabic{enumiv}]}{%
    \settowidth\labelwidth{[#1]}%
    \leftmargin\labelwidth
    \advance\leftmargin\labelsep
    \usecounter{enumiv}%
    \let\p@enumiv\@empty
    \renewcommand\theenumiv{\arabic{enumiv}}%
  }%
  \sloppy
  \clubpenalty4000
  \@clubpenalty \clubpenalty
  \widowpenalty4000
  \sfcode`\.=\@m
}{%
  \def\@noitemerr{\@latex@warning{Empty `thebibliography' environment}}%
  \endlist
}
