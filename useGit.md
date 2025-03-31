# Git学习

## 一.初始操作

1. 创建本地仓库和远程仓库，并将两个仓库连接起来：
   `git init  #初始化`
   `git remote add origin ssh连接`
   一般情况下，git中自动创建一个master分支，如果需要在此基础上更新代码，则可以使用：
   `git checkout -b develop`
   来创建一个名为develop（可以任意命名此分支）的分支，更新代码。
2. 更新完成之后使用 `git add .`将所有代码添加到暂存区，然后使用 `git commit -m "加入你的注释"`完成一次代码提交
3. 使用命令 `git checkout master`切换回master分支，然后输入：`git merge develop`完成代码合并
4. 将代码推送到GitHub：
`git push origin master`


## 二.其他问题
### 导入github中其他分支的代码：
使用`git fetch origin`拉去远程仓库,，然后 `git reset --hard master`把其他分支的东西强制下在到本地，如果master分支和main分支无共同交集，按理此时无法将修改后的代码传入main分支，需要输入 `git pull origin main --allow-unrelated-histories`来强制把main分支的文件下载入本地，之后则正常修改即可.

### master和main
wsl下的linux中输入`git init`时，默认的分支是master，而相同的操作在windows下，则为main。GitHub中，默认的分支是main。（所以我目前的两个项目，都有一个master分支，因为最开始使用linux去进行操作的）
