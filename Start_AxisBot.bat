@echo off
chcp 65001 >nul
echo ========================================
echo    Axis Data Quality Bot v3.1
echo    Đang khởi động Backend + Frontend...
echo ========================================
echo.

:: Khởi động Backend
start cmd /k "cd backend && uvicorn main:app --reload --port 8000"

:: Chờ 3 giây
timeout /t 3 /nobreak >nul

:: Khởi động Frontend
start cmd /k "cd frontend && streamlit run app.py"

echo.
echo ✅ Đã mở Axis Bot thành công!
echo    Frontend: http://localhost:8501
echo    (Không đóng 2 cửa sổ CMD này)
echo.
pause