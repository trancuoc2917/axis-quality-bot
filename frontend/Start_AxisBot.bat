@echo off
chcp 65001 >nul
title Axis Data Quality Bot v3.1 - Professional Mode

echo ========================================
echo    Axis Data Quality Bot v3.1
echo    Đang khởi động...
echo ========================================

:: Khởi động Backend
start "Axis Backend" cmd /k "cd backend && uvicorn main:app --host 127.0.0.1 --port 8000 --no-reload"

timeout /t 4 /nobreak >nul

:: Khởi động Frontend
start "Axis Frontend" cmd /k "cd frontend && streamlit run app.py --server.headless true"

echo.
echo ✅ Bot đã khởi động thành công!
echo 🌐 Mở trình duyệt và truy cập: http://localhost:8501
echo.
echo Nhấn Ctrl + C trong cửa sổ này để dừng bot.
pause