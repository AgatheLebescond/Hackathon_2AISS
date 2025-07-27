@echo off
title LANCEMENT IA DOC SEARCH

REM === Activer l'environnement virtuel
call .\venv\Scripts\activate

REM === Lancer l'interface Streamlit
start "Streamlit" cmd /k streamlit run frontend.py

REM === Lancer le Watcher (surveillance de fichiers)
start "Watcher" cmd /k python automation\watcher.py

REM === Ouvrir l’interface dans le navigateur
start http://localhost:8501

echo Application en cours d'exécution...
pause
