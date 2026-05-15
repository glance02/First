# Repository Guidelines

## 项目结构与职责
当前分支是一个计算机学院课程报告的 LaTeX 模板/正文项目。

- `main.tex`：文档入口，只负责设置课程名、引入摘要/正文/参考文献等章节文件，不在这里堆正文内容。
- `csreport.cls`：课程报告类文件，封装页面、字体、页眉、目录、标题、摘要、图表公式编号和参考文献格式。
- `chapter/`：正文内容目录。摘要、绪论、正文主体、结论等都放在这里，并由 `main.tex` 用 `\input{chapter/...}` 引入。
- `references.bib`：BibTeX 参考文献数据库，放在仓库根目录，由 `main.tex` 中的 `\bibliography{references}` 引入。
- `img/`：报告图片资源目录，正文中用相对路径引用。
- `template.md`：课程报告撰写规范的文本参考。
- `latex.ps1`：本项目的 XeLaTeX 编译脚本。

封面、扉页、教师评语页不由当前 `main.tex` 和 `csreport.cls` 生成，除非用户明确要求，不要主动加入这些页面。

## 编译与验证
在仓库根目录执行：

```powershell
.\latex.ps1
```

脚本会依次运行 XeLaTeX、BibTeX、XeLaTeX、XeLaTeX，以刷新目录、页码、交叉引用和参考文献。修改 `main.tex`、`csreport.cls`、`chapter/*.tex` 或 `references.bib` 后，至少运行一次 `.\latex.ps1` 验证是否能生成 `main.pdf`。

如果用户没有提示要进行编译tex，请不要主动执行编译命令。

## LaTeX 写作规则
- 正文内容优先写入 `chapter/*.tex`，不要把大段正文直接写进 `main.tex`。
- 新增章节时，先在 `chapter/` 下创建简洁的文件名，再在 `main.tex` 中添加对应 `\input{chapter/文件名}`。
- 中文正文使用规范中文标点；英文摘要和英文关键词保持英文标点。
- 图片放入 `img/`，正文中使用 `\includegraphics` 引用相对路径。
- 参考文献统一写入根目录 `references.bib`，不要在各章节末尾分散放参考文献，也不要再手写 `thebibliography`。
- 标题层级使用 `\section`、`\subsection`、`\subsubsection`，不要手写编号。
- 图、表、公式编号由 `csreport.cls` 自动处理，正文中不要手写“图2.1”“表2.1”等编号。
- 代码使用minted环境，保持代码块清晰。

## 模板维护规则
- 修改版式、字体、页眉、目录、标题、摘要环境等全局格式时，优先改 `csreport.cls`。
- 修改具体报告内容时，只改 `chapter/*.tex`。
- `\coursename{...}` 在 `main.tex` 中设置，用于页眉显示 `《课程名》课程报告`。
- 保持模板面向 XeLaTeX，不要改成 pdfLaTeX 编译。
- 不要引入复杂构建系统；当前项目保持 `latex.ps1` 作为唯一编译入口。

## 生成物与 Git
- `.aux`、`.log`、`.toc`、`.synctex.gz` 等 LaTeX 中间文件是生成物，不要手工编辑。
- `main.pdf` 是编译产物；是否提交按用户要求处理。
- 工作区可能包含用户未提交的改动。修改前先查看相关文件，避免覆盖用户内容。
- 不要执行 `git reset --hard`、强制清理或删除用户文件，除非用户明确要求。
