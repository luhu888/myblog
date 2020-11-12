git branch 查看当前项目有几个分支
git branch dev  本地创建分支
git checkout dev 本地切换到dev分支
git add .
git commit -m "init dev"
git .ignore没有生效的解决办法：git清除本地缓存
git rm -r --cached .
git add .
git commit -m 'update .gitignore'
git push -u origin master

git push origin dev     将dev分支推到远程仓库
git fetch code 拉取远程仓库的其他分支代码（我拉代码是remote add code所以这里是code,可以用git remote查看）
git checkout 分支A 切换到分支A
git pull code 分支A 拉取分支A代码
git checkout 分支B 切换到分支B
git pull code 分支B 拉取分支B代码
git merge --no-ff 分支A 将分支A合并到分支B
git status 查看冲突代码
eclipse解决冲突代码
git push code 分支B 提交解决冲突后的代码