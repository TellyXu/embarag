@echo on
cd %~dp0
echo Setting up Python environment...
cmd /c "pip install -r requirements.txt > nul 2>&1"

echo Starting RAG application...
start /B cmd /c "cd backend && python main.py > nul 2>&1"

echo Starting frontend application...
start /B cmd /c "cd frontend && npm install > nul 2>&1 && npm start > nul 2>&1"
