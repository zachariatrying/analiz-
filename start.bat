@echo off
REM IPO Analyzer Baslatma Scripti

REM Proje klasorune git (Eger farkli bir yerdeysek)
cd /d "C:\Users\ibrah\.gemini\antigravity\scratch\ipo_analyzer"

REM Uygulamayi calistir
echo IPO Analyzer Baslatiliyor...
echo Lutfen tarayicinin acilmasini bekleyin...
python -m streamlit run src/app.py

pause
