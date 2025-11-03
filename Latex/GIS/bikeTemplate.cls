% bikeTemplate.cls
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{bikeTemplate}[2025/11/03 Custom class for bike sharing report]

% --- 基于 article 类 ---
\LoadClass[12pt,a4paper]{article}

% --- 编码与中文支持 ---
\RequirePackage{xeCJK}
\RequirePackage{fontspec}
% \setCJKmainfont{Microsoft YaHei}
% 如果系统没有 Microsoft YaHei，可按需改为 SimSun 或者 
\setCJKmainfont[BoldFont={SimHei}]{SimSun}

% --- 页面布局与微调 ---
\RequirePackage[a4paper,margin=2.5cm]{geometry}
\RequirePackage{setspace}
\onehalfspacing
\RequirePackage{indentfirst}
\setlength{\parindent}{2em}
\setlength{\parskip}{0.5em}
\setlength{\headheight}{14.5pt}

% --- 常用包 ---
\RequirePackage{amsmath}
\RequirePackage{graphicx}
\RequirePackage{enumitem}
\RequirePackage{hyperref}
\hypersetup{colorlinks=true, linkcolor=black, urlcolor=blue, citecolor=blue}
\RequirePackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{中国矿业大学}
\fancyhead[R]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}

\RequirePackage{float}
% bibliography style 由主文件设置

% --- 目录样式优化 ---
\RequirePackage{tocloft}
\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}
\renewcommand{\cftsecfont}{\bfseries}
\renewcommand{\cftsecpagefont}{\bfseries\large}
\setlength{\cftbeforesecskip}{0.8em}

% --- 标题与章节样式微调 ---
\RequirePackage{titlesec}
\titleformat{\section}{\Large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\large\bfseries}{\thesubsection}{1em}{}

% --- 标题重定义 ---
\renewcommand{\contentsname}{目录}
\renewcommand{\refname}{参考文献}
\renewcommand{\figurename}{图}
