@echo on
cd %~dp0
echo Setting up Python environment...
cmd /c "pip install -r requirements.txt > nul 2>&1"

echo Starting RAG application...
start cmd /c "cd backend && uvicorn main:app --reload"

echo Starting frontend application...
start cmd /c "cd frontend && npm install && npm start"
