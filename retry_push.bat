@echo off
echo 🔄 开始持续重试 git push...
echo 按 Ctrl+C 可以停止重试
echo.

set /a count=1

:retry
echo [%time%] 第 %count% 次尝试...
git push origin feat/venue-management
if %errorlevel% equ 0 (
    echo.
    echo ✅ 推送成功！
    echo 🎉 feat/venue-management 分支已成功推送到远程仓库
    pause
    exit /b 0
) else (
    echo ❌ 推送失败，等待 5 秒后重试...
    timeout /t 5 /nobreak >nul
    set /a count+=1
    goto retry
)