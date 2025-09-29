# Git学习

## 常用指令

### **常规操作**

1. 创建本地仓库和远程仓库，并将两个仓库连接起来：

   ```bash
   git init  #初始化`
   git remote add origin ssh连接 #将远程分支命名为origin
   ```

   一般情况下，git中自动创建一个master分支。

2. 创建一个名为develop（可以任意命名此分支）的分支，更新代码。 `git checkout -b develop` 可以再此分支上对代码进行修改。

3. `git status` 查看修改的状态。

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

6. 将代码推送到GitHub： `git push origin master`

### 其他基础指令

#### 版本控制

1. 版本回退。直接会回到对应版本的状态，这个状态之后的部分则不显示。 `git reset --hard commitID`

2. `git reflog` 查看所有的版本控制，可以看到已经删除的提交记录。

#### 分支

1. `git branch`查看分支

   1. `-a`参数，表示查看所有分支（包括远端和本地分支)，

   2. `-r`表示查看远端分支

   3. 直接添加一串字符，表示自动创建以该字符为名的分支

   4. `git branch -d <branch-name>`删除本地分支。`-d`参数若改成`-D`，则是强制删除

   5. `git push origin --delete <branch-name>`删除远程分支

2. `git checkout 分支名`切换到对应分支

   1. `-b`表示如若没有该分支，则创建该分支，并且切换到该分支。需在分支名前面使用该参数，如：`git checkout -b develop`

3. `git merge <branch-name>` 合并分支。把branch-name分支的东西合并到当前所在的分支中。如果有冲突，则进入冲突文件，解决冲突之后，再重新add、commit一次。

## 笔记

### git rebase

git rebase是用来对分支进行合并的命令，它可以把一个分支的提交历史变成另一个分支的提交历史。

1. 使用`rebase`

```bash
git checkout feature
git rebase master
```

切换到feature分支，然后把master的提交历史合并到feature分支的提交历史。

1. 出现冲突 如果出现冲突，会提示你先解决冲突，如`warning: Cannot merge binary files: readme.md (HEAD vs. 81a5937 (Add Feature A))`则说明文件readme.md存在冲突，需要手动解决冲突。正常解决即可。 解决之后，可以有一些指令：

   - `git add.` 将所有文件添加到暂存区

   - `git rebase --continue` 继续合并

   - `git rebase --abort` 放弃合并

   - `git rebase --skip` 跳过当前提交，继续下一个提交

2. 交互式`rebase`

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

### 关于.gitignore文件

直接将不需要追踪的文件写在.gitignore文件中即可，支持通配符表示。但是.gitignore对已经追踪的文件不起作用，意思是说不会删除之前已经上传过的部分。可以如下操作：

1. `git ls-files` 查看缓存中的所有文件

2. `git rm -r --cache *exe dist\` 其中-r表示递归删除，即可以删除文件夹，--cache表示删除缓存中的文件而不影响本地文件，再在右边加上需要在缓存中删除的文件即可

3. 之后再正常提交和push就可以了。

## 其他问题

### 导入github中其他分支的代码：

使用`git fetch origin`拉去远程仓库,，然后 `git reset --hard master`把其他分支的东西强制下在到本地，如果master分支和main分支无共同交集，按理此时无法将修改后的代码传入main分支，需要输入 `git pull origin main --allow-unrelated-histories`来强制把main分支的文件下载入本地，之后则正常修改即可。