# Repository Guidelines

## 项目结构与职责
这是一个基于 XeLaTeX 的计算机学院课程报告模板/正文项目。文档入口使用 `ctexart`，通用格式集中在样式包中，正文按章节拆分维护。

- `main.tex`：文档入口，只负责引入 `reportstyle.sty`、设置报告标题、组织摘要/目录/正文/参考文献/附录等章节文件，不在这里堆正文内容。
- `reportstyle.sty`：通用课程报告样式包，封装页面、行距、页眉页脚、标题、图表、列表、超链接、代码块、提示框、摘要和关键词等格式。
- `chapter/`：正文内容目录。摘要、绪论、正文主体、结论、附录等都放在这里，并由 `main.tex` 用 `\input{chapter/...}` 引入。
- `references.bib`：BibTeX 参考文献数据库，放在仓库根目录，由 `main.tex` 中的 `\bibliography{references}` 引入。
- `Img/`：报告图片资源目录，正文中用相对路径引用。
- `template.md`：课程报告撰写规范的文本参考。
- `latex.ps1`：本项目的 XeLaTeX 编译脚本。

封面、扉页、教师评语页不由当前 `main.tex` 和 `reportstyle.sty` 生成，除非用户明确要求，不要主动加入这些页面。

## 编译与验证
在仓库根目录执行：

```powershell
.\latex.ps1
```

如果用户没有提示要进行编译tex，请不要主动执行编译命令。

## LaTeX 写作规则
- 正文内容优先写入 `chapter/*.tex`，不要把大段正文直接写进 `main.tex`。
- 新增章节时，先在 `chapter/` 下创建简洁的文件名，再在 `main.tex` 中添加对应 `\input{chapter/文件名}`。
- 中文正文使用规范中文标点；英文摘要和英文关键词保持英文标点。
- 图片放入 `Img/`，正文中使用 `\includegraphics` 引用相对路径。
- 参考文献统一写入根目录 `references.bib`，不要在各章节末尾分散放参考文献，也不要再手写 `thebibliography`。
- 标题层级使用 `\section`、`\subsection`、`\subsubsection`，不要手写编号。
- 图、表、公式编号由 LaTeX 自动处理，正文中不要手写“图2.1”“表2.1”等编号。
- 摘要写在 `chapter/abstract.tex`，中文摘要使用 `abstractcn` 环境和 `\keywords{...}`，英文摘要使用 `abstracten` 环境和 `\enkeywords{...}`。
- 代码使用 `minted` 环境，保持代码块清晰。由于 `minted` 需要 shell escape，编译入口保持使用 `latex.ps1`。

## 模板维护规则
- 修改版式、字体、页眉、目录、标题、摘要环境等全局格式时，优先改 `reportstyle.sty`。
- 修改具体报告内容时，只改 `chapter/*.tex`。
- `\reporttitle{...}` 在 `main.tex` 中设置，用于页眉显示报告标题。
- 保持模板面向 XeLaTeX，不要改成 pdfLaTeX 编译。
- 不要引入复杂构建系统；当前项目保持 `latex.ps1` 作为唯一编译入口。

## 生成物与 Git
- `.aux`、`.log`、`.toc`、`.synctex.gz` 等 LaTeX 中间文件是生成物，不要手工编辑。
- `main.pdf` 是编译产物；是否提交按用户要求处理。
- 工作区可能包含用户未提交的改动。修改前先查看相关文件，避免覆盖用户内容。
- 不要执行 `git reset --hard`、强制清理或删除用户文件，除非用户明确要求。
