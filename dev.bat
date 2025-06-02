@echo off
echo 🔧 Starting Bot Development Mode
echo ========================================
echo 🔄 Auto-restart enabled
echo 🛑 Press Ctrl+C to stop
echo ========================================

:loop
python run.py
echo.
echo 🔄 Bot stopped. Press any key to restart or Ctrl+C to exit...
pause >nul
goto loop
