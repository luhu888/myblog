git branch 查看当前项目有几个分支
git branch dev  本地创建分支
git checkout dev 本地切换到dev分支
git add .
git commit -m "init dev"
git .ignore没有生效的解决办法：git清除本地缓存
git rm -r --cached .
git add ./new 添加修改的文件
git commit -m 'update .gitignore'
git push -u origin master //第一次提交才需要写这么长，后续直接git push就可以

git push origin dev     将dev分支推到远程仓库
git fetch code 拉取远程仓库的其他分支代码（我拉代码是remote add code所以这里是code,可以用git remote查看）
git checkout 分支A 切换到分支A
git pull code 分支A 拉取分支A代码
git checkout 分支B 切换到分支B
git pull code 分支B 拉取分支B代码
git merge --no-ff 分支A 将分支A合并到分支B
git status 查看冲突代码
git push code 分支B 提交解决冲突后的代码

git remote -v 查看远程仓库
git fetch upstream 拉取上游最新代码
git merge upstream/tests 合并上游拉下来的最新代码与本地test2分支代码
git push origin local_branch:remote_branch  推送到指定远程分支
删除本地已合并的分支： git branch -d [branchname]