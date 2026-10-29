@echo off
title PROLOG-C - Compiler Design Lab Studio Launcher
echo ======================================================================
echo    Starting PROLOG-C: Compiler Design & Logic Inference Studio
echo    Course: 22PC2CS301 (Compiler Design & CN Laboratory)
echo    College: VNR Vignana Jyothi Institute of Engineering & Technology
echo ======================================================================
echo.
echo Launching PROLOG-C Compiler Studio on Port 5050...
start "PROLOG-C Compiler Studio (Port 5050)" cmd /k "python app.py"

echo.
echo Studio started successfully!
echo Open your browser and navigate to: http://127.0.0.1:5050
echo.
pause
