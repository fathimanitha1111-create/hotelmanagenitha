@echo off
echo ====================================================
echo Pushing hotelmanagenitha to GitHub...
echo ====================================================
cd /d "%~dp0"
git push -u origin main
if %ERRORLEVEL% equ 0 (
    echo.
    echo ====================================================
    echo [SUCCESS] Your code has been pushed to GitHub!
    echo You can now go to Vercel and redeploy.
    echo ====================================================
) else (
    echo.
    echo ====================================================
    echo [FAILED] Push failed. Please check the error above.
    echo ====================================================
)
pause
