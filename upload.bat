@echo off
echo 正在上传代码到GitHub...

cd /d C:\Users\27631\WeChatProjects\miniprogram-4

echo 当前分支:
git branch

echo.
echo 配置SSH远程仓库:
git remote set-url origin git@github.com:codesoldier99/UAVexam_site_backend.git

echo.
echo 检查状态:
git status

echo.
echo 添加所有文件:
git add .

echo.
echo 提交更改:
git commit -m "Add WeChat miniprogram code" --allow-empty

echo.
echo 推送到远程仓库:
git push origin miniprogram

echo.
echo 上传完成！
pause