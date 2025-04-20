# Git学习
## 初始操作
1. 创建本地仓库和远程仓库，并将两个仓库连接起来：
   ```bash
   git init  #初始化`
   git remote add origin ssh连接
   ```
   一般情况下，git中自动创建一个master分支。
2. 创建一个名为develop（可以任意命名此分支）的分支，更新代码。
   `git checkout -b develop`
   可以再此分支上对代码进行修改。

4. 更新完成之后,输入如下代码完成一次代码提交
    ```bash
   git add . #将所有代码添加到暂存区，然后使用 `
   git commit -m "注释"
    ```
    
5. 使用命令切换回master分支，然后完成代码合并
   ```bash
    git checkout master
    git merge develop
   ```

6. 将代码推送到GitHub：
   `git push origin master`

## 笔记
### git rebase
git rebase是用来对分支进行合并的命令，它可以把一个分支的提交历史变成另一个分支的提交历史。

1. 使用`rebase`
```bash
git checkout feature
git rebase master
```
切换到feature分支，然后把master的提交历史合并到feature分支的提交历史。

2. 出现冲突
如果出现冲突，会提示你先解决冲突，如`warning: Cannot merge binary files: readme.md (HEAD vs. 81a5937 (Add Feature A))`则说明文件readme.md存在冲突，需要手动解决冲突。正常解决即可。
解决之后，可以有一些指令：
   - `git add.` 将所有文件添加到暂存区
   - `git rebase --continue` 继续合并
   - `git rebase --abort` 放弃合并
   - `git rebase --skip` 跳过当前提交，继续下一个提交

3. 交互式`rebase`
```bash
git rebase -i HEAD~3
```
显示当前分支的前3条git记录:

![](pic/2025-04-15-23-28-46.png)

*常用操作指令*：
   - `pick`：保留提交
   - `reword`：修改提交信息
   - `edit`：修改提交内容
   - `squash`：合并到前一个提交
   - `fixup` ：合并并丢弃提交信息
   - `drop` ：删除提交



## 其他问题
### 导入github中其他分支的代码：
使用`git fetch origin`拉去远程仓库,，然后 `git reset --hard master`把其他分支的东西强制下在到本地，如果master分支和main分支无共同交集，按理此时无法将修改后的代码传入main分支，需要输入 `git pull origin main --allow-unrelated-histories`来强制把main分支的文件下载入本地，之后则正常修改即可。

sdadasda

# vim技巧
## 编辑
### 常规插入
- i，即insert，在光标前插入内容，并进入插入模式
- a，即append，在光标后插入内容，并进入插入模式
- o，即open，在当前行下方插入新行，并进入插入模式
 
### `c`(change)的用法
- cc，即change current line，删除当前行，并进入插入模式(即S)
- cw，即change word，删除光标所在的单词，并进入插入模式
- ci"，删除双引号内的内容，并进入插入模式(同样的，把"换成(或者其他也行)
 

## 移动
### 单词间移动
- w，移动到下一个单词的开头
- e，移动到下一个单词的结尾
- b，移动到上一个单词的开头
- }，移动到下一个段落的开头
- {，移动到上一个段落的开头
- fa,找到a(把a改成其他也行)

### 行间移动
- j，向下移动一行
- k，向上移动一行
- }，移动到下一个段落的开头
- {，移动到上一个段落的开头
- ctr+d，向下翻半页
- ctr+u，向上翻半页
- gg，移动到文件开头
- G，移动到文件末尾

### 屏幕移动
- zz，将当前行移动到屏幕的中间
- zt，将当前行移动到屏幕的顶部
- zb，将当前行移动到屏幕的底部

### EasyMoiton移动
- \\fa,找到a，之后再输入对应字母，就能直接跳转了

